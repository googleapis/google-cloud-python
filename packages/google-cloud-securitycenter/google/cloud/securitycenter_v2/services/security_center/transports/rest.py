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
from google.protobuf import json_format
import grpc  # type: ignore
from requests import __version__ as requests_version

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault, None]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object, None]  # type: ignore


from google.iam.v1 import iam_policy_pb2  # type: ignore
from google.iam.v1 import policy_pb2  # type: ignore
from google.longrunning import operations_pb2  # type: ignore
from google.protobuf import empty_pb2  # type: ignore

from google.cloud.securitycenter_v2.types import securitycenter_service, simulation
from google.cloud.securitycenter_v2.types import external_system as gcs_external_system
from google.cloud.securitycenter_v2.types import (
    notification_config as gcs_notification_config,
)
from google.cloud.securitycenter_v2.types import (
    resource_value_config as gcs_resource_value_config,
)
from google.cloud.securitycenter_v2.types import security_marks as gcs_security_marks
from google.cloud.securitycenter_v2.types import bigquery_export
from google.cloud.securitycenter_v2.types import finding
from google.cloud.securitycenter_v2.types import finding as gcs_finding
from google.cloud.securitycenter_v2.types import mute_config
from google.cloud.securitycenter_v2.types import mute_config as gcs_mute_config
from google.cloud.securitycenter_v2.types import notification_config
from google.cloud.securitycenter_v2.types import resource_value_config
from google.cloud.securitycenter_v2.types import source
from google.cloud.securitycenter_v2.types import source as gcs_source
from google.cloud.securitycenter_v2.types import valued_resource

from .base import DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO
from .base import SecurityCenterTransport

DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=BASE_DEFAULT_CLIENT_INFO.gapic_version,
    grpc_version=None,
    rest_version=requests_version,
)


class SecurityCenterRestInterceptor:
    """Interceptor for SecurityCenter.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the SecurityCenterRestTransport.

    .. code-block:: python
        class MyCustomSecurityCenterInterceptor(SecurityCenterRestInterceptor):
            def pre_batch_create_resource_value_configs(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_batch_create_resource_value_configs(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_bulk_mute_findings(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_bulk_mute_findings(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_big_query_export(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_big_query_export(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_finding(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_finding(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_mute_config(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_mute_config(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_notification_config(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_notification_config(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_create_source(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_source(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_delete_big_query_export(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def pre_delete_mute_config(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def pre_delete_notification_config(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def pre_delete_resource_value_config(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def pre_get_big_query_export(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_big_query_export(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_iam_policy(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_iam_policy(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_mute_config(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_mute_config(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_notification_config(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_notification_config(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_resource_value_config(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_resource_value_config(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_simulation(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_simulation(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_source(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_source(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_get_valued_resource(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_valued_resource(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_group_findings(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_group_findings(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_attack_paths(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_attack_paths(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_big_query_exports(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_big_query_exports(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_findings(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_findings(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_mute_configs(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_mute_configs(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_notification_configs(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_notification_configs(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_resource_value_configs(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_resource_value_configs(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_sources(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_sources(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_list_valued_resources(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_valued_resources(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_set_finding_state(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_set_finding_state(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_set_iam_policy(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_set_iam_policy(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_set_mute(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_set_mute(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_test_iam_permissions(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_test_iam_permissions(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_big_query_export(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_big_query_export(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_external_system(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_external_system(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_finding(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_finding(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_mute_config(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_mute_config(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_notification_config(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_notification_config(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_resource_value_config(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_resource_value_config(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_security_marks(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_security_marks(self, response):
                logging.log(f"Received response: {response}")
                return response

            def pre_update_source(self, request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_source(self, response):
                logging.log(f"Received response: {response}")
                return response

        transport = SecurityCenterRestTransport(interceptor=MyCustomSecurityCenterInterceptor())
        client = SecurityCenterClient(transport=transport)


    """

    def pre_batch_create_resource_value_configs(
        self,
        request: securitycenter_service.BatchCreateResourceValueConfigsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        securitycenter_service.BatchCreateResourceValueConfigsRequest,
        Sequence[Tuple[str, str]],
    ]:
        """Pre-rpc interceptor for batch_create_resource_value_configs

        Override in a subclass to manipulate the request or metadata
        before they are sent to the SecurityCenter server.
        """
        return request, metadata

    def post_batch_create_resource_value_configs(
        self, response: securitycenter_service.BatchCreateResourceValueConfigsResponse
    ) -> securitycenter_service.BatchCreateResourceValueConfigsResponse:
        """Post-rpc interceptor for batch_create_resource_value_configs

        Override in a subclass to manipulate the response
        after it is returned by the SecurityCenter server but before
        it is returned to user code.
        """
        return response

    def pre_bulk_mute_findings(
        self,
        request: securitycenter_service.BulkMuteFindingsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        securitycenter_service.BulkMuteFindingsRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for bulk_mute_findings

        Override in a subclass to manipulate the request or metadata
        before they are sent to the SecurityCenter server.
        """
        return request, metadata

    def post_bulk_mute_findings(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for bulk_mute_findings

        Override in a subclass to manipulate the response
        after it is returned by the SecurityCenter server but before
        it is returned to user code.
        """
        return response

    def pre_create_big_query_export(
        self,
        request: securitycenter_service.CreateBigQueryExportRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        securitycenter_service.CreateBigQueryExportRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for create_big_query_export

        Override in a subclass to manipulate the request or metadata
        before they are sent to the SecurityCenter server.
        """
        return request, metadata

    def post_create_big_query_export(
        self, response: bigquery_export.BigQueryExport
    ) -> bigquery_export.BigQueryExport:
        """Post-rpc interceptor for create_big_query_export

        Override in a subclass to manipulate the response
        after it is returned by the SecurityCenter server but before
        it is returned to user code.
        """
        return response

    def pre_create_finding(
        self,
        request: securitycenter_service.CreateFindingRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[securitycenter_service.CreateFindingRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_finding

        Override in a subclass to manipulate the request or metadata
        before they are sent to the SecurityCenter server.
        """
        return request, metadata

    def post_create_finding(self, response: gcs_finding.Finding) -> gcs_finding.Finding:
        """Post-rpc interceptor for create_finding

        Override in a subclass to manipulate the response
        after it is returned by the SecurityCenter server but before
        it is returned to user code.
        """
        return response

    def pre_create_mute_config(
        self,
        request: securitycenter_service.CreateMuteConfigRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        securitycenter_service.CreateMuteConfigRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for create_mute_config

        Override in a subclass to manipulate the request or metadata
        before they are sent to the SecurityCenter server.
        """
        return request, metadata

    def post_create_mute_config(
        self, response: gcs_mute_config.MuteConfig
    ) -> gcs_mute_config.MuteConfig:
        """Post-rpc interceptor for create_mute_config

        Override in a subclass to manipulate the response
        after it is returned by the SecurityCenter server but before
        it is returned to user code.
        """
        return response

    def pre_create_notification_config(
        self,
        request: securitycenter_service.CreateNotificationConfigRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        securitycenter_service.CreateNotificationConfigRequest,
        Sequence[Tuple[str, str]],
    ]:
        """Pre-rpc interceptor for create_notification_config

        Override in a subclass to manipulate the request or metadata
        before they are sent to the SecurityCenter server.
        """
        return request, metadata

    def post_create_notification_config(
        self, response: gcs_notification_config.NotificationConfig
    ) -> gcs_notification_config.NotificationConfig:
        """Post-rpc interceptor for create_notification_config

        Override in a subclass to manipulate the response
        after it is returned by the SecurityCenter server but before
        it is returned to user code.
        """
        return response

    def pre_create_source(
        self,
        request: securitycenter_service.CreateSourceRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[securitycenter_service.CreateSourceRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_source

        Override in a subclass to manipulate the request or metadata
        before they are sent to the SecurityCenter server.
        """
        return request, metadata

    def post_create_source(self, response: gcs_source.Source) -> gcs_source.Source:
        """Post-rpc interceptor for create_source

        Override in a subclass to manipulate the response
        after it is returned by the SecurityCenter server but before
        it is returned to user code.
        """
        return response

    def pre_delete_big_query_export(
        self,
        request: securitycenter_service.DeleteBigQueryExportRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        securitycenter_service.DeleteBigQueryExportRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for delete_big_query_export

        Override in a subclass to manipulate the request or metadata
        before they are sent to the SecurityCenter server.
        """
        return request, metadata

    def pre_delete_mute_config(
        self,
        request: securitycenter_service.DeleteMuteConfigRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        securitycenter_service.DeleteMuteConfigRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for delete_mute_config

        Override in a subclass to manipulate the request or metadata
        before they are sent to the SecurityCenter server.
        """
        return request, metadata

    def pre_delete_notification_config(
        self,
        request: securitycenter_service.DeleteNotificationConfigRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        securitycenter_service.DeleteNotificationConfigRequest,
        Sequence[Tuple[str, str]],
    ]:
        """Pre-rpc interceptor for delete_notification_config

        Override in a subclass to manipulate the request or metadata
        before they are sent to the SecurityCenter server.
        """
        return request, metadata

    def pre_delete_resource_value_config(
        self,
        request: securitycenter_service.DeleteResourceValueConfigRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        securitycenter_service.DeleteResourceValueConfigRequest,
        Sequence[Tuple[str, str]],
    ]:
        """Pre-rpc interceptor for delete_resource_value_config

        Override in a subclass to manipulate the request or metadata
        before they are sent to the SecurityCenter server.
        """
        return request, metadata

    def pre_get_big_query_export(
        self,
        request: securitycenter_service.GetBigQueryExportRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        securitycenter_service.GetBigQueryExportRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for get_big_query_export

        Override in a subclass to manipulate the request or metadata
        before they are sent to the SecurityCenter server.
        """
        return request, metadata

    def post_get_big_query_export(
        self, response: bigquery_export.BigQueryExport
    ) -> bigquery_export.BigQueryExport:
        """Post-rpc interceptor for get_big_query_export

        Override in a subclass to manipulate the response
        after it is returned by the SecurityCenter server but before
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
        before they are sent to the SecurityCenter server.
        """
        return request, metadata

    def post_get_iam_policy(self, response: policy_pb2.Policy) -> policy_pb2.Policy:
        """Post-rpc interceptor for get_iam_policy

        Override in a subclass to manipulate the response
        after it is returned by the SecurityCenter server but before
        it is returned to user code.
        """
        return response

    def pre_get_mute_config(
        self,
        request: securitycenter_service.GetMuteConfigRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[securitycenter_service.GetMuteConfigRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_mute_config

        Override in a subclass to manipulate the request or metadata
        before they are sent to the SecurityCenter server.
        """
        return request, metadata

    def post_get_mute_config(
        self, response: mute_config.MuteConfig
    ) -> mute_config.MuteConfig:
        """Post-rpc interceptor for get_mute_config

        Override in a subclass to manipulate the response
        after it is returned by the SecurityCenter server but before
        it is returned to user code.
        """
        return response

    def pre_get_notification_config(
        self,
        request: securitycenter_service.GetNotificationConfigRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        securitycenter_service.GetNotificationConfigRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for get_notification_config

        Override in a subclass to manipulate the request or metadata
        before they are sent to the SecurityCenter server.
        """
        return request, metadata

    def post_get_notification_config(
        self, response: notification_config.NotificationConfig
    ) -> notification_config.NotificationConfig:
        """Post-rpc interceptor for get_notification_config

        Override in a subclass to manipulate the response
        after it is returned by the SecurityCenter server but before
        it is returned to user code.
        """
        return response

    def pre_get_resource_value_config(
        self,
        request: securitycenter_service.GetResourceValueConfigRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        securitycenter_service.GetResourceValueConfigRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for get_resource_value_config

        Override in a subclass to manipulate the request or metadata
        before they are sent to the SecurityCenter server.
        """
        return request, metadata

    def post_get_resource_value_config(
        self, response: resource_value_config.ResourceValueConfig
    ) -> resource_value_config.ResourceValueConfig:
        """Post-rpc interceptor for get_resource_value_config

        Override in a subclass to manipulate the response
        after it is returned by the SecurityCenter server but before
        it is returned to user code.
        """
        return response

    def pre_get_simulation(
        self,
        request: securitycenter_service.GetSimulationRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[securitycenter_service.GetSimulationRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_simulation

        Override in a subclass to manipulate the request or metadata
        before they are sent to the SecurityCenter server.
        """
        return request, metadata

    def post_get_simulation(
        self, response: simulation.Simulation
    ) -> simulation.Simulation:
        """Post-rpc interceptor for get_simulation

        Override in a subclass to manipulate the response
        after it is returned by the SecurityCenter server but before
        it is returned to user code.
        """
        return response

    def pre_get_source(
        self,
        request: securitycenter_service.GetSourceRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[securitycenter_service.GetSourceRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_source

        Override in a subclass to manipulate the request or metadata
        before they are sent to the SecurityCenter server.
        """
        return request, metadata

    def post_get_source(self, response: source.Source) -> source.Source:
        """Post-rpc interceptor for get_source

        Override in a subclass to manipulate the response
        after it is returned by the SecurityCenter server but before
        it is returned to user code.
        """
        return response

    def pre_get_valued_resource(
        self,
        request: securitycenter_service.GetValuedResourceRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        securitycenter_service.GetValuedResourceRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for get_valued_resource

        Override in a subclass to manipulate the request or metadata
        before they are sent to the SecurityCenter server.
        """
        return request, metadata

    def post_get_valued_resource(
        self, response: valued_resource.ValuedResource
    ) -> valued_resource.ValuedResource:
        """Post-rpc interceptor for get_valued_resource

        Override in a subclass to manipulate the response
        after it is returned by the SecurityCenter server but before
        it is returned to user code.
        """
        return response

    def pre_group_findings(
        self,
        request: securitycenter_service.GroupFindingsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[securitycenter_service.GroupFindingsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for group_findings

        Override in a subclass to manipulate the request or metadata
        before they are sent to the SecurityCenter server.
        """
        return request, metadata

    def post_group_findings(
        self, response: securitycenter_service.GroupFindingsResponse
    ) -> securitycenter_service.GroupFindingsResponse:
        """Post-rpc interceptor for group_findings

        Override in a subclass to manipulate the response
        after it is returned by the SecurityCenter server but before
        it is returned to user code.
        """
        return response

    def pre_list_attack_paths(
        self,
        request: securitycenter_service.ListAttackPathsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        securitycenter_service.ListAttackPathsRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for list_attack_paths

        Override in a subclass to manipulate the request or metadata
        before they are sent to the SecurityCenter server.
        """
        return request, metadata

    def post_list_attack_paths(
        self, response: securitycenter_service.ListAttackPathsResponse
    ) -> securitycenter_service.ListAttackPathsResponse:
        """Post-rpc interceptor for list_attack_paths

        Override in a subclass to manipulate the response
        after it is returned by the SecurityCenter server but before
        it is returned to user code.
        """
        return response

    def pre_list_big_query_exports(
        self,
        request: securitycenter_service.ListBigQueryExportsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        securitycenter_service.ListBigQueryExportsRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for list_big_query_exports

        Override in a subclass to manipulate the request or metadata
        before they are sent to the SecurityCenter server.
        """
        return request, metadata

    def post_list_big_query_exports(
        self, response: securitycenter_service.ListBigQueryExportsResponse
    ) -> securitycenter_service.ListBigQueryExportsResponse:
        """Post-rpc interceptor for list_big_query_exports

        Override in a subclass to manipulate the response
        after it is returned by the SecurityCenter server but before
        it is returned to user code.
        """
        return response

    def pre_list_findings(
        self,
        request: securitycenter_service.ListFindingsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[securitycenter_service.ListFindingsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_findings

        Override in a subclass to manipulate the request or metadata
        before they are sent to the SecurityCenter server.
        """
        return request, metadata

    def post_list_findings(
        self, response: securitycenter_service.ListFindingsResponse
    ) -> securitycenter_service.ListFindingsResponse:
        """Post-rpc interceptor for list_findings

        Override in a subclass to manipulate the response
        after it is returned by the SecurityCenter server but before
        it is returned to user code.
        """
        return response

    def pre_list_mute_configs(
        self,
        request: securitycenter_service.ListMuteConfigsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        securitycenter_service.ListMuteConfigsRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for list_mute_configs

        Override in a subclass to manipulate the request or metadata
        before they are sent to the SecurityCenter server.
        """
        return request, metadata

    def post_list_mute_configs(
        self, response: securitycenter_service.ListMuteConfigsResponse
    ) -> securitycenter_service.ListMuteConfigsResponse:
        """Post-rpc interceptor for list_mute_configs

        Override in a subclass to manipulate the response
        after it is returned by the SecurityCenter server but before
        it is returned to user code.
        """
        return response

    def pre_list_notification_configs(
        self,
        request: securitycenter_service.ListNotificationConfigsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        securitycenter_service.ListNotificationConfigsRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for list_notification_configs

        Override in a subclass to manipulate the request or metadata
        before they are sent to the SecurityCenter server.
        """
        return request, metadata

    def post_list_notification_configs(
        self, response: securitycenter_service.ListNotificationConfigsResponse
    ) -> securitycenter_service.ListNotificationConfigsResponse:
        """Post-rpc interceptor for list_notification_configs

        Override in a subclass to manipulate the response
        after it is returned by the SecurityCenter server but before
        it is returned to user code.
        """
        return response

    def pre_list_resource_value_configs(
        self,
        request: securitycenter_service.ListResourceValueConfigsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        securitycenter_service.ListResourceValueConfigsRequest,
        Sequence[Tuple[str, str]],
    ]:
        """Pre-rpc interceptor for list_resource_value_configs

        Override in a subclass to manipulate the request or metadata
        before they are sent to the SecurityCenter server.
        """
        return request, metadata

    def post_list_resource_value_configs(
        self, response: securitycenter_service.ListResourceValueConfigsResponse
    ) -> securitycenter_service.ListResourceValueConfigsResponse:
        """Post-rpc interceptor for list_resource_value_configs

        Override in a subclass to manipulate the response
        after it is returned by the SecurityCenter server but before
        it is returned to user code.
        """
        return response

    def pre_list_sources(
        self,
        request: securitycenter_service.ListSourcesRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[securitycenter_service.ListSourcesRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_sources

        Override in a subclass to manipulate the request or metadata
        before they are sent to the SecurityCenter server.
        """
        return request, metadata

    def post_list_sources(
        self, response: securitycenter_service.ListSourcesResponse
    ) -> securitycenter_service.ListSourcesResponse:
        """Post-rpc interceptor for list_sources

        Override in a subclass to manipulate the response
        after it is returned by the SecurityCenter server but before
        it is returned to user code.
        """
        return response

    def pre_list_valued_resources(
        self,
        request: securitycenter_service.ListValuedResourcesRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        securitycenter_service.ListValuedResourcesRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for list_valued_resources

        Override in a subclass to manipulate the request or metadata
        before they are sent to the SecurityCenter server.
        """
        return request, metadata

    def post_list_valued_resources(
        self, response: securitycenter_service.ListValuedResourcesResponse
    ) -> securitycenter_service.ListValuedResourcesResponse:
        """Post-rpc interceptor for list_valued_resources

        Override in a subclass to manipulate the response
        after it is returned by the SecurityCenter server but before
        it is returned to user code.
        """
        return response

    def pre_set_finding_state(
        self,
        request: securitycenter_service.SetFindingStateRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        securitycenter_service.SetFindingStateRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for set_finding_state

        Override in a subclass to manipulate the request or metadata
        before they are sent to the SecurityCenter server.
        """
        return request, metadata

    def post_set_finding_state(self, response: finding.Finding) -> finding.Finding:
        """Post-rpc interceptor for set_finding_state

        Override in a subclass to manipulate the response
        after it is returned by the SecurityCenter server but before
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
        before they are sent to the SecurityCenter server.
        """
        return request, metadata

    def post_set_iam_policy(self, response: policy_pb2.Policy) -> policy_pb2.Policy:
        """Post-rpc interceptor for set_iam_policy

        Override in a subclass to manipulate the response
        after it is returned by the SecurityCenter server but before
        it is returned to user code.
        """
        return response

    def pre_set_mute(
        self,
        request: securitycenter_service.SetMuteRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[securitycenter_service.SetMuteRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for set_mute

        Override in a subclass to manipulate the request or metadata
        before they are sent to the SecurityCenter server.
        """
        return request, metadata

    def post_set_mute(self, response: finding.Finding) -> finding.Finding:
        """Post-rpc interceptor for set_mute

        Override in a subclass to manipulate the response
        after it is returned by the SecurityCenter server but before
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
        before they are sent to the SecurityCenter server.
        """
        return request, metadata

    def post_test_iam_permissions(
        self, response: iam_policy_pb2.TestIamPermissionsResponse
    ) -> iam_policy_pb2.TestIamPermissionsResponse:
        """Post-rpc interceptor for test_iam_permissions

        Override in a subclass to manipulate the response
        after it is returned by the SecurityCenter server but before
        it is returned to user code.
        """
        return response

    def pre_update_big_query_export(
        self,
        request: securitycenter_service.UpdateBigQueryExportRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        securitycenter_service.UpdateBigQueryExportRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for update_big_query_export

        Override in a subclass to manipulate the request or metadata
        before they are sent to the SecurityCenter server.
        """
        return request, metadata

    def post_update_big_query_export(
        self, response: bigquery_export.BigQueryExport
    ) -> bigquery_export.BigQueryExport:
        """Post-rpc interceptor for update_big_query_export

        Override in a subclass to manipulate the response
        after it is returned by the SecurityCenter server but before
        it is returned to user code.
        """
        return response

    def pre_update_external_system(
        self,
        request: securitycenter_service.UpdateExternalSystemRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        securitycenter_service.UpdateExternalSystemRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for update_external_system

        Override in a subclass to manipulate the request or metadata
        before they are sent to the SecurityCenter server.
        """
        return request, metadata

    def post_update_external_system(
        self, response: gcs_external_system.ExternalSystem
    ) -> gcs_external_system.ExternalSystem:
        """Post-rpc interceptor for update_external_system

        Override in a subclass to manipulate the response
        after it is returned by the SecurityCenter server but before
        it is returned to user code.
        """
        return response

    def pre_update_finding(
        self,
        request: securitycenter_service.UpdateFindingRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[securitycenter_service.UpdateFindingRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_finding

        Override in a subclass to manipulate the request or metadata
        before they are sent to the SecurityCenter server.
        """
        return request, metadata

    def post_update_finding(self, response: gcs_finding.Finding) -> gcs_finding.Finding:
        """Post-rpc interceptor for update_finding

        Override in a subclass to manipulate the response
        after it is returned by the SecurityCenter server but before
        it is returned to user code.
        """
        return response

    def pre_update_mute_config(
        self,
        request: securitycenter_service.UpdateMuteConfigRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        securitycenter_service.UpdateMuteConfigRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for update_mute_config

        Override in a subclass to manipulate the request or metadata
        before they are sent to the SecurityCenter server.
        """
        return request, metadata

    def post_update_mute_config(
        self, response: gcs_mute_config.MuteConfig
    ) -> gcs_mute_config.MuteConfig:
        """Post-rpc interceptor for update_mute_config

        Override in a subclass to manipulate the response
        after it is returned by the SecurityCenter server but before
        it is returned to user code.
        """
        return response

    def pre_update_notification_config(
        self,
        request: securitycenter_service.UpdateNotificationConfigRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        securitycenter_service.UpdateNotificationConfigRequest,
        Sequence[Tuple[str, str]],
    ]:
        """Pre-rpc interceptor for update_notification_config

        Override in a subclass to manipulate the request or metadata
        before they are sent to the SecurityCenter server.
        """
        return request, metadata

    def post_update_notification_config(
        self, response: gcs_notification_config.NotificationConfig
    ) -> gcs_notification_config.NotificationConfig:
        """Post-rpc interceptor for update_notification_config

        Override in a subclass to manipulate the response
        after it is returned by the SecurityCenter server but before
        it is returned to user code.
        """
        return response

    def pre_update_resource_value_config(
        self,
        request: securitycenter_service.UpdateResourceValueConfigRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        securitycenter_service.UpdateResourceValueConfigRequest,
        Sequence[Tuple[str, str]],
    ]:
        """Pre-rpc interceptor for update_resource_value_config

        Override in a subclass to manipulate the request or metadata
        before they are sent to the SecurityCenter server.
        """
        return request, metadata

    def post_update_resource_value_config(
        self, response: gcs_resource_value_config.ResourceValueConfig
    ) -> gcs_resource_value_config.ResourceValueConfig:
        """Post-rpc interceptor for update_resource_value_config

        Override in a subclass to manipulate the response
        after it is returned by the SecurityCenter server but before
        it is returned to user code.
        """
        return response

    def pre_update_security_marks(
        self,
        request: securitycenter_service.UpdateSecurityMarksRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[
        securitycenter_service.UpdateSecurityMarksRequest, Sequence[Tuple[str, str]]
    ]:
        """Pre-rpc interceptor for update_security_marks

        Override in a subclass to manipulate the request or metadata
        before they are sent to the SecurityCenter server.
        """
        return request, metadata

    def post_update_security_marks(
        self, response: gcs_security_marks.SecurityMarks
    ) -> gcs_security_marks.SecurityMarks:
        """Post-rpc interceptor for update_security_marks

        Override in a subclass to manipulate the response
        after it is returned by the SecurityCenter server but before
        it is returned to user code.
        """
        return response

    def pre_update_source(
        self,
        request: securitycenter_service.UpdateSourceRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[securitycenter_service.UpdateSourceRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_source

        Override in a subclass to manipulate the request or metadata
        before they are sent to the SecurityCenter server.
        """
        return request, metadata

    def post_update_source(self, response: gcs_source.Source) -> gcs_source.Source:
        """Post-rpc interceptor for update_source

        Override in a subclass to manipulate the response
        after it is returned by the SecurityCenter server but before
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
        before they are sent to the SecurityCenter server.
        """
        return request, metadata

    def post_cancel_operation(self, response: None) -> None:
        """Post-rpc interceptor for cancel_operation

        Override in a subclass to manipulate the response
        after it is returned by the SecurityCenter server but before
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
        before they are sent to the SecurityCenter server.
        """
        return request, metadata

    def post_delete_operation(self, response: None) -> None:
        """Post-rpc interceptor for delete_operation

        Override in a subclass to manipulate the response
        after it is returned by the SecurityCenter server but before
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
        before they are sent to the SecurityCenter server.
        """
        return request, metadata

    def post_get_operation(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for get_operation

        Override in a subclass to manipulate the response
        after it is returned by the SecurityCenter server but before
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
        before they are sent to the SecurityCenter server.
        """
        return request, metadata

    def post_list_operations(
        self, response: operations_pb2.ListOperationsResponse
    ) -> operations_pb2.ListOperationsResponse:
        """Post-rpc interceptor for list_operations

        Override in a subclass to manipulate the response
        after it is returned by the SecurityCenter server but before
        it is returned to user code.
        """
        return response


@dataclasses.dataclass
class SecurityCenterRestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: SecurityCenterRestInterceptor


class SecurityCenterRestTransport(SecurityCenterTransport):
    """REST backend transport for SecurityCenter.

    V2 APIs for Security Center service.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends JSON representations of protocol buffers over HTTP/1.1

    """

    def __init__(
        self,
        *,
        host: str = "securitycenter.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        client_cert_source_for_mtls: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
        url_scheme: str = "https",
        interceptor: Optional[SecurityCenterRestInterceptor] = None,
        api_audience: Optional[str] = None,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]):
                 The hostname to connect to (default: 'securitycenter.googleapis.com').
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
        self._interceptor = interceptor or SecurityCenterRestInterceptor()
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
                        "uri": "/v2/{name=organizations/*/operations/*}:cancel",
                    },
                ],
                "google.longrunning.Operations.DeleteOperation": [
                    {
                        "method": "delete",
                        "uri": "/v2/{name=organizations/*/operations/*}",
                    },
                ],
                "google.longrunning.Operations.GetOperation": [
                    {
                        "method": "get",
                        "uri": "/v2/{name=organizations/*/operations/*}",
                    },
                ],
                "google.longrunning.Operations.ListOperations": [
                    {
                        "method": "get",
                        "uri": "/v2/{name=organizations/*/operations}",
                    },
                ],
            }

            rest_transport = operations_v1.OperationsRestTransport(
                host=self._host,
                # use the credentials which are saved
                credentials=self._credentials,
                scopes=self._scopes,
                http_options=http_options,
                path_prefix="v2",
            )

            self._operations_client = operations_v1.AbstractOperationsClient(
                transport=rest_transport
            )

        # Return the client from cache.
        return self._operations_client

    class _BatchCreateResourceValueConfigs(SecurityCenterRestStub):
        def __hash__(self):
            return hash("BatchCreateResourceValueConfigs")

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
            request: securitycenter_service.BatchCreateResourceValueConfigsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> securitycenter_service.BatchCreateResourceValueConfigsResponse:
            r"""Call the batch create resource
            value configs method over HTTP.

                Args:
                    request (~.securitycenter_service.BatchCreateResourceValueConfigsRequest):
                        The request object. Request message to create multiple
                    resource value configs
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.securitycenter_service.BatchCreateResourceValueConfigsResponse:
                        Response message for
                    BatchCreateResourceValueConfigs

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v2/{parent=organizations/*}/resourceValueConfigs:batchCreate",
                    "body": "*",
                },
                {
                    "method": "post",
                    "uri": "/v2/{parent=organizations/*/locations/*}/resourceValueConfigs:batchCreate",
                    "body": "*",
                },
            ]
            (
                request,
                metadata,
            ) = self._interceptor.pre_batch_create_resource_value_configs(
                request, metadata
            )
            pb_request = (
                securitycenter_service.BatchCreateResourceValueConfigsRequest.pb(
                    request
                )
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
            resp = securitycenter_service.BatchCreateResourceValueConfigsResponse()
            pb_resp = securitycenter_service.BatchCreateResourceValueConfigsResponse.pb(
                resp
            )

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_batch_create_resource_value_configs(resp)
            return resp

    class _BulkMuteFindings(SecurityCenterRestStub):
        def __hash__(self):
            return hash("BulkMuteFindings")

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
            request: securitycenter_service.BulkMuteFindingsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the bulk mute findings method over HTTP.

            Args:
                request (~.securitycenter_service.BulkMuteFindingsRequest):
                    The request object. Request message for bulk findings
                update.
                Note:

                1. If multiple bulk update requests
                    match the same resource, the order
                    in which they get executed is not
                    defined.
                2. Once a bulk operation is started,
                    there is no way to stop it.
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
                    "uri": "/v2/{parent=organizations/*}/findings:bulkMute",
                    "body": "*",
                },
                {
                    "method": "post",
                    "uri": "/v2/{parent=organizations/*/locations/*}/findings:bulkMute",
                    "body": "*",
                },
                {
                    "method": "post",
                    "uri": "/v2/{parent=folders/*}/findings:bulkMute",
                    "body": "*",
                },
                {
                    "method": "post",
                    "uri": "/v2/{parent=folders/*/locations/*}/findings:bulkMute",
                    "body": "*",
                },
                {
                    "method": "post",
                    "uri": "/v2/{parent=projects/*}/findings:bulkMute",
                    "body": "*",
                },
                {
                    "method": "post",
                    "uri": "/v2/{parent=projects/*/locations/*}/findings:bulkMute",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_bulk_mute_findings(
                request, metadata
            )
            pb_request = securitycenter_service.BulkMuteFindingsRequest.pb(request)
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
            resp = self._interceptor.post_bulk_mute_findings(resp)
            return resp

    class _CreateBigQueryExport(SecurityCenterRestStub):
        def __hash__(self):
            return hash("CreateBigQueryExport")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {
            "bigQueryExportId": "",
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
            request: securitycenter_service.CreateBigQueryExportRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> bigquery_export.BigQueryExport:
            r"""Call the create big query export method over HTTP.

            Args:
                request (~.securitycenter_service.CreateBigQueryExportRequest):
                    The request object. Request message for creating a
                BigQuery export.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.bigquery_export.BigQueryExport:
                    Configures how to deliver Findings to
                BigQuery Instance.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v2/{parent=organizations/*/locations/*}/bigQueryExports",
                    "body": "big_query_export",
                },
                {
                    "method": "post",
                    "uri": "/v2/{parent=folders/*/locations/*}/bigQueryExports",
                    "body": "big_query_export",
                },
                {
                    "method": "post",
                    "uri": "/v2/{parent=projects/*/locations/*}/bigQueryExports",
                    "body": "big_query_export",
                },
            ]
            request, metadata = self._interceptor.pre_create_big_query_export(
                request, metadata
            )
            pb_request = securitycenter_service.CreateBigQueryExportRequest.pb(request)
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
            resp = bigquery_export.BigQueryExport()
            pb_resp = bigquery_export.BigQueryExport.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_big_query_export(resp)
            return resp

    class _CreateFinding(SecurityCenterRestStub):
        def __hash__(self):
            return hash("CreateFinding")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {
            "findingId": "",
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
            request: securitycenter_service.CreateFindingRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> gcs_finding.Finding:
            r"""Call the create finding method over HTTP.

            Args:
                request (~.securitycenter_service.CreateFindingRequest):
                    The request object. Request message for creating a
                finding.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.gcs_finding.Finding:
                    Security Command Center finding.

                A finding is a record of assessment data
                like security, risk, health, or privacy,
                that is ingested into Security Command
                Center for presentation, notification,
                analysis, policy testing, and
                enforcement. For example, a cross-site
                scripting (XSS) vulnerability in an App
                Engine application is a finding.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v2/{parent=organizations/*/sources/*/locations/*}/findings",
                    "body": "finding",
                },
                {
                    "method": "post",
                    "uri": "/v2/{parent=organizations/*/sources/*}/findings",
                    "body": "finding",
                },
            ]
            request, metadata = self._interceptor.pre_create_finding(request, metadata)
            pb_request = securitycenter_service.CreateFindingRequest.pb(request)
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
            resp = gcs_finding.Finding()
            pb_resp = gcs_finding.Finding.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_finding(resp)
            return resp

    class _CreateMuteConfig(SecurityCenterRestStub):
        def __hash__(self):
            return hash("CreateMuteConfig")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {
            "muteConfigId": "",
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
            request: securitycenter_service.CreateMuteConfigRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> gcs_mute_config.MuteConfig:
            r"""Call the create mute config method over HTTP.

            Args:
                request (~.securitycenter_service.CreateMuteConfigRequest):
                    The request object. Request message for creating a mute
                config.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.gcs_mute_config.MuteConfig:
                    A mute config is a Cloud SCC resource
                that contains the configuration to mute
                create/update events of findings.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v2/{parent=organizations/*/locations/*}/muteConfigs",
                    "body": "mute_config",
                },
                {
                    "method": "post",
                    "uri": "/v2/{parent=folders/*/locations/*}/muteConfigs",
                    "body": "mute_config",
                },
                {
                    "method": "post",
                    "uri": "/v2/{parent=projects/*/locations/*}/muteConfigs",
                    "body": "mute_config",
                },
                {
                    "method": "post",
                    "uri": "/v2/{parent=organizations/*}/muteConfigs",
                    "body": "mute_config",
                },
                {
                    "method": "post",
                    "uri": "/v2/{parent=folders/*}/muteConfigs",
                    "body": "mute_config",
                },
                {
                    "method": "post",
                    "uri": "/v2/{parent=projects/*}/muteConfigs",
                    "body": "mute_config",
                },
            ]
            request, metadata = self._interceptor.pre_create_mute_config(
                request, metadata
            )
            pb_request = securitycenter_service.CreateMuteConfigRequest.pb(request)
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
            resp = gcs_mute_config.MuteConfig()
            pb_resp = gcs_mute_config.MuteConfig.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_mute_config(resp)
            return resp

    class _CreateNotificationConfig(SecurityCenterRestStub):
        def __hash__(self):
            return hash("CreateNotificationConfig")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, Any] = {
            "configId": "",
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
            request: securitycenter_service.CreateNotificationConfigRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> gcs_notification_config.NotificationConfig:
            r"""Call the create notification
            config method over HTTP.

                Args:
                    request (~.securitycenter_service.CreateNotificationConfigRequest):
                        The request object. Request message for creating a
                    notification config.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.gcs_notification_config.NotificationConfig:
                        Cloud Security Command Center (Cloud
                    SCC) notification configs.
                    A notification config is a Cloud SCC
                    resource that contains the configuration
                    to send notifications for create/update
                    events of findings, assets and etc.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v2/{parent=organizations/*/locations/*}/notificationConfigs",
                    "body": "notification_config",
                },
                {
                    "method": "post",
                    "uri": "/v2/{parent=folders/*/locations/*}/notificationConfigs",
                    "body": "notification_config",
                },
                {
                    "method": "post",
                    "uri": "/v2/{parent=projects/*/locations/*}/notificationConfigs",
                    "body": "notification_config",
                },
            ]
            request, metadata = self._interceptor.pre_create_notification_config(
                request, metadata
            )
            pb_request = securitycenter_service.CreateNotificationConfigRequest.pb(
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
            resp = gcs_notification_config.NotificationConfig()
            pb_resp = gcs_notification_config.NotificationConfig.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_notification_config(resp)
            return resp

    class _CreateSource(SecurityCenterRestStub):
        def __hash__(self):
            return hash("CreateSource")

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
            request: securitycenter_service.CreateSourceRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> gcs_source.Source:
            r"""Call the create source method over HTTP.

            Args:
                request (~.securitycenter_service.CreateSourceRequest):
                    The request object. Request message for creating a
                source.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.gcs_source.Source:
                    Security Command Center finding
                source. A finding source is an entity or
                a mechanism that can produce a finding.
                A source is like a container of findings
                that come from the same scanner, logger,
                monitor, and other tools.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v2/{parent=organizations/*}/sources",
                    "body": "source",
                },
            ]
            request, metadata = self._interceptor.pre_create_source(request, metadata)
            pb_request = securitycenter_service.CreateSourceRequest.pb(request)
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
            resp = gcs_source.Source()
            pb_resp = gcs_source.Source.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_source(resp)
            return resp

    class _DeleteBigQueryExport(SecurityCenterRestStub):
        def __hash__(self):
            return hash("DeleteBigQueryExport")

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
            request: securitycenter_service.DeleteBigQueryExportRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ):
            r"""Call the delete big query export method over HTTP.

            Args:
                request (~.securitycenter_service.DeleteBigQueryExportRequest):
                    The request object. Request message for deleting a
                BigQuery export.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "delete",
                    "uri": "/v2/{name=organizations/*/locations/*/bigQueryExports/*}",
                },
                {
                    "method": "delete",
                    "uri": "/v2/{name=folders/*/locations/*/bigQueryExports/*}",
                },
                {
                    "method": "delete",
                    "uri": "/v2/{name=projects/*/locations/*/bigQueryExports/*}",
                },
            ]
            request, metadata = self._interceptor.pre_delete_big_query_export(
                request, metadata
            )
            pb_request = securitycenter_service.DeleteBigQueryExportRequest.pb(request)
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

    class _DeleteMuteConfig(SecurityCenterRestStub):
        def __hash__(self):
            return hash("DeleteMuteConfig")

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
            request: securitycenter_service.DeleteMuteConfigRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ):
            r"""Call the delete mute config method over HTTP.

            Args:
                request (~.securitycenter_service.DeleteMuteConfigRequest):
                    The request object. Request message for deleting a mute
                config. If no location is specified,
                default is global.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "delete",
                    "uri": "/v2/{name=organizations/*/muteConfigs/*}",
                },
                {
                    "method": "delete",
                    "uri": "/v2/{name=organizations/*/locations/*/muteConfigs/*}",
                },
                {
                    "method": "delete",
                    "uri": "/v2/{name=folders/*/muteConfigs/*}",
                },
                {
                    "method": "delete",
                    "uri": "/v2/{name=folders/*/locations/*/muteConfigs/*}",
                },
                {
                    "method": "delete",
                    "uri": "/v2/{name=projects/*/muteConfigs/*}",
                },
                {
                    "method": "delete",
                    "uri": "/v2/{name=projects/*/locations/*/muteConfigs/*}",
                },
            ]
            request, metadata = self._interceptor.pre_delete_mute_config(
                request, metadata
            )
            pb_request = securitycenter_service.DeleteMuteConfigRequest.pb(request)
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

    class _DeleteNotificationConfig(SecurityCenterRestStub):
        def __hash__(self):
            return hash("DeleteNotificationConfig")

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
            request: securitycenter_service.DeleteNotificationConfigRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ):
            r"""Call the delete notification
            config method over HTTP.

                Args:
                    request (~.securitycenter_service.DeleteNotificationConfigRequest):
                        The request object. Request message for deleting a
                    notification config.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "delete",
                    "uri": "/v2/{name=organizations/*/locations/*/notificationConfigs/*}",
                },
                {
                    "method": "delete",
                    "uri": "/v2/{name=folders/*/locations/*/notificationConfigs/*}",
                },
                {
                    "method": "delete",
                    "uri": "/v2/{name=projects/*/locations/*/notificationConfigs/*}",
                },
            ]
            request, metadata = self._interceptor.pre_delete_notification_config(
                request, metadata
            )
            pb_request = securitycenter_service.DeleteNotificationConfigRequest.pb(
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

    class _DeleteResourceValueConfig(SecurityCenterRestStub):
        def __hash__(self):
            return hash("DeleteResourceValueConfig")

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
            request: securitycenter_service.DeleteResourceValueConfigRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ):
            r"""Call the delete resource value
            config method over HTTP.

                Args:
                    request (~.securitycenter_service.DeleteResourceValueConfigRequest):
                        The request object. Request message to delete resource
                    value config
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "delete",
                    "uri": "/v2/{name=organizations/*/resourceValueConfigs/*}",
                },
                {
                    "method": "delete",
                    "uri": "/v2/{name=organizations/*/locations/*/resourceValueConfigs/*}",
                },
            ]
            request, metadata = self._interceptor.pre_delete_resource_value_config(
                request, metadata
            )
            pb_request = securitycenter_service.DeleteResourceValueConfigRequest.pb(
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

    class _GetBigQueryExport(SecurityCenterRestStub):
        def __hash__(self):
            return hash("GetBigQueryExport")

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
            request: securitycenter_service.GetBigQueryExportRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> bigquery_export.BigQueryExport:
            r"""Call the get big query export method over HTTP.

            Args:
                request (~.securitycenter_service.GetBigQueryExportRequest):
                    The request object. Request message for retrieving a
                BigQuery export.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.bigquery_export.BigQueryExport:
                    Configures how to deliver Findings to
                BigQuery Instance.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v2/{name=organizations/*/locations/*/bigQueryExports/*}",
                },
                {
                    "method": "get",
                    "uri": "/v2/{name=folders/*/locations/*/bigQueryExports/*}",
                },
                {
                    "method": "get",
                    "uri": "/v2/{name=projects/*/locations/*/bigQueryExports/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_big_query_export(
                request, metadata
            )
            pb_request = securitycenter_service.GetBigQueryExportRequest.pb(request)
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
            resp = bigquery_export.BigQueryExport()
            pb_resp = bigquery_export.BigQueryExport.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_big_query_export(resp)
            return resp

    class _GetIamPolicy(SecurityCenterRestStub):
        def __hash__(self):
            return hash("GetIamPolicy")

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
            request: iam_policy_pb2.GetIamPolicyRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> policy_pb2.Policy:
            r"""Call the get iam policy method over HTTP.

            Args:
                request (~.iam_policy_pb2.GetIamPolicyRequest):
                    The request object. Request message for ``GetIamPolicy`` method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

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

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v2/{resource=organizations/*/sources/*}:getIamPolicy",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_get_iam_policy(request, metadata)
            pb_request = request
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
            resp = policy_pb2.Policy()
            pb_resp = resp

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_iam_policy(resp)
            return resp

    class _GetMuteConfig(SecurityCenterRestStub):
        def __hash__(self):
            return hash("GetMuteConfig")

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
            request: securitycenter_service.GetMuteConfigRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> mute_config.MuteConfig:
            r"""Call the get mute config method over HTTP.

            Args:
                request (~.securitycenter_service.GetMuteConfigRequest):
                    The request object. Request message for retrieving a mute
                config. If no location is specified,
                default is global.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.mute_config.MuteConfig:
                    A mute config is a Cloud SCC resource
                that contains the configuration to mute
                create/update events of findings.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v2/{name=organizations/*/muteConfigs/*}",
                },
                {
                    "method": "get",
                    "uri": "/v2/{name=organizations/*/locations/*/muteConfigs/*}",
                },
                {
                    "method": "get",
                    "uri": "/v2/{name=folders/*/muteConfigs/*}",
                },
                {
                    "method": "get",
                    "uri": "/v2/{name=folders/*/locations/*/muteConfigs/*}",
                },
                {
                    "method": "get",
                    "uri": "/v2/{name=projects/*/muteConfigs/*}",
                },
                {
                    "method": "get",
                    "uri": "/v2/{name=projects/*/locations/*/muteConfigs/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_mute_config(request, metadata)
            pb_request = securitycenter_service.GetMuteConfigRequest.pb(request)
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
            resp = mute_config.MuteConfig()
            pb_resp = mute_config.MuteConfig.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_mute_config(resp)
            return resp

    class _GetNotificationConfig(SecurityCenterRestStub):
        def __hash__(self):
            return hash("GetNotificationConfig")

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
            request: securitycenter_service.GetNotificationConfigRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> notification_config.NotificationConfig:
            r"""Call the get notification config method over HTTP.

            Args:
                request (~.securitycenter_service.GetNotificationConfigRequest):
                    The request object. Request message for getting a
                notification config.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.notification_config.NotificationConfig:
                    Cloud Security Command Center (Cloud
                SCC) notification configs.
                A notification config is a Cloud SCC
                resource that contains the configuration
                to send notifications for create/update
                events of findings, assets and etc.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v2/{name=organizations/*/locations/*/notificationConfigs/*}",
                },
                {
                    "method": "get",
                    "uri": "/v2/{name=folders/*/locations/*/notificationConfigs/*}",
                },
                {
                    "method": "get",
                    "uri": "/v2/{name=projects/*/locations/*/notificationConfigs/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_notification_config(
                request, metadata
            )
            pb_request = securitycenter_service.GetNotificationConfigRequest.pb(request)
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
            resp = notification_config.NotificationConfig()
            pb_resp = notification_config.NotificationConfig.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_notification_config(resp)
            return resp

    class _GetResourceValueConfig(SecurityCenterRestStub):
        def __hash__(self):
            return hash("GetResourceValueConfig")

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
            request: securitycenter_service.GetResourceValueConfigRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> resource_value_config.ResourceValueConfig:
            r"""Call the get resource value config method over HTTP.

            Args:
                request (~.securitycenter_service.GetResourceValueConfigRequest):
                    The request object. Request message to get resource value
                config
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.resource_value_config.ResourceValueConfig:
                    A resource value configuration (RVC)
                is a mapping configuration of user's
                resources to resource values. Used in
                Attack path simulations.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v2/{name=organizations/*/resourceValueConfigs/*}",
                },
                {
                    "method": "get",
                    "uri": "/v2/{name=organizations/*/locations/*/resourceValueConfigs/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_resource_value_config(
                request, metadata
            )
            pb_request = securitycenter_service.GetResourceValueConfigRequest.pb(
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
            resp = resource_value_config.ResourceValueConfig()
            pb_resp = resource_value_config.ResourceValueConfig.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_resource_value_config(resp)
            return resp

    class _GetSimulation(SecurityCenterRestStub):
        def __hash__(self):
            return hash("GetSimulation")

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
            request: securitycenter_service.GetSimulationRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> simulation.Simulation:
            r"""Call the get simulation method over HTTP.

            Args:
                request (~.securitycenter_service.GetSimulationRequest):
                    The request object. Request message for getting
                simulation. Simulation name can include
                "latest" to retrieve the latest
                simulation For example,
                "organizations/123/simulations/latest".
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.simulation.Simulation:
                    Attack path simulation
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v2/{name=organizations/*/simulations/*}",
                },
                {
                    "method": "get",
                    "uri": "/v2/{name=organizations/*/locations/*/simulations/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_simulation(request, metadata)
            pb_request = securitycenter_service.GetSimulationRequest.pb(request)
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
            resp = simulation.Simulation()
            pb_resp = simulation.Simulation.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_simulation(resp)
            return resp

    class _GetSource(SecurityCenterRestStub):
        def __hash__(self):
            return hash("GetSource")

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
            request: securitycenter_service.GetSourceRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> source.Source:
            r"""Call the get source method over HTTP.

            Args:
                request (~.securitycenter_service.GetSourceRequest):
                    The request object. Request message for getting a source.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.source.Source:
                    Security Command Center finding
                source. A finding source is an entity or
                a mechanism that can produce a finding.
                A source is like a container of findings
                that come from the same scanner, logger,
                monitor, and other tools.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v2/{name=organizations/*/sources/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_source(request, metadata)
            pb_request = securitycenter_service.GetSourceRequest.pb(request)
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
            resp = source.Source()
            pb_resp = source.Source.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_source(resp)
            return resp

    class _GetValuedResource(SecurityCenterRestStub):
        def __hash__(self):
            return hash("GetValuedResource")

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
            request: securitycenter_service.GetValuedResourceRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> valued_resource.ValuedResource:
            r"""Call the get valued resource method over HTTP.

            Args:
                request (~.securitycenter_service.GetValuedResourceRequest):
                    The request object. Request message for getting a valued
                resource.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.valued_resource.ValuedResource:
                    A resource that is determined to have
                value to a user's system

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v2/{name=organizations/*/simulations/*/valuedResources/*}",
                },
                {
                    "method": "get",
                    "uri": "/v2/{name=organizations/*/locations/*/simulations/*/valuedResources/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_valued_resource(
                request, metadata
            )
            pb_request = securitycenter_service.GetValuedResourceRequest.pb(request)
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
            resp = valued_resource.ValuedResource()
            pb_resp = valued_resource.ValuedResource.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_valued_resource(resp)
            return resp

    class _GroupFindings(SecurityCenterRestStub):
        def __hash__(self):
            return hash("GroupFindings")

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
            request: securitycenter_service.GroupFindingsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> securitycenter_service.GroupFindingsResponse:
            r"""Call the group findings method over HTTP.

            Args:
                request (~.securitycenter_service.GroupFindingsRequest):
                    The request object. Request message for grouping by
                findings.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.securitycenter_service.GroupFindingsResponse:
                    Response message for group by
                findings.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v2/{parent=organizations/*/sources/*}/findings:group",
                    "body": "*",
                },
                {
                    "method": "post",
                    "uri": "/v2/{parent=organizations/*/sources/*/locations/*}/findings:group",
                    "body": "*",
                },
                {
                    "method": "post",
                    "uri": "/v2/{parent=folders/*/sources/*}/findings:group",
                    "body": "*",
                },
                {
                    "method": "post",
                    "uri": "/v2/{parent=folders/*/sources/*/locations/*}/findings:group",
                    "body": "*",
                },
                {
                    "method": "post",
                    "uri": "/v2/{parent=projects/*/sources/*}/findings:group",
                    "body": "*",
                },
                {
                    "method": "post",
                    "uri": "/v2/{parent=projects/*/sources/*/locations/*}/findings:group",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_group_findings(request, metadata)
            pb_request = securitycenter_service.GroupFindingsRequest.pb(request)
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
            resp = securitycenter_service.GroupFindingsResponse()
            pb_resp = securitycenter_service.GroupFindingsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_group_findings(resp)
            return resp

    class _ListAttackPaths(SecurityCenterRestStub):
        def __hash__(self):
            return hash("ListAttackPaths")

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
            request: securitycenter_service.ListAttackPathsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> securitycenter_service.ListAttackPathsResponse:
            r"""Call the list attack paths method over HTTP.

            Args:
                request (~.securitycenter_service.ListAttackPathsRequest):
                    The request object. Request message for listing the
                attack paths for a given simulation or
                valued resource.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.securitycenter_service.ListAttackPathsResponse:
                    Response message for listing the
                attack paths for a given simulation or
                valued resource.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v2/{parent=organizations/*/simulations/*}/attackPaths",
                },
                {
                    "method": "get",
                    "uri": "/v2/{parent=organizations/*/simulations/*/valuedResources/*}/attackPaths",
                },
                {
                    "method": "get",
                    "uri": "/v2/{parent=organizations/*/locations/*/simulations/*/valuedResources/*}/attackPaths",
                },
                {
                    "method": "get",
                    "uri": "/v2/{parent=organizations/*/simulations/*/attackExposureResults/*}/attackPaths",
                },
                {
                    "method": "get",
                    "uri": "/v2/{parent=organizations/*/locations/*/simulations/*/attackExposureResults/*}/attackPaths",
                },
            ]
            request, metadata = self._interceptor.pre_list_attack_paths(
                request, metadata
            )
            pb_request = securitycenter_service.ListAttackPathsRequest.pb(request)
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
            resp = securitycenter_service.ListAttackPathsResponse()
            pb_resp = securitycenter_service.ListAttackPathsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_attack_paths(resp)
            return resp

    class _ListBigQueryExports(SecurityCenterRestStub):
        def __hash__(self):
            return hash("ListBigQueryExports")

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
            request: securitycenter_service.ListBigQueryExportsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> securitycenter_service.ListBigQueryExportsResponse:
            r"""Call the list big query exports method over HTTP.

            Args:
                request (~.securitycenter_service.ListBigQueryExportsRequest):
                    The request object. Request message for listing BigQuery
                exports at a given scope e.g.
                organization, folder or project.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.securitycenter_service.ListBigQueryExportsResponse:
                    Response message for listing BigQuery
                exports.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v2/{parent=organizations/*/locations/*}/bigQueryExports",
                },
                {
                    "method": "get",
                    "uri": "/v2/{parent=folders/*/locations/*}/bigQueryExports",
                },
                {
                    "method": "get",
                    "uri": "/v2/{parent=projects/*/locations/*}/bigQueryExports",
                },
            ]
            request, metadata = self._interceptor.pre_list_big_query_exports(
                request, metadata
            )
            pb_request = securitycenter_service.ListBigQueryExportsRequest.pb(request)
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
            resp = securitycenter_service.ListBigQueryExportsResponse()
            pb_resp = securitycenter_service.ListBigQueryExportsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_big_query_exports(resp)
            return resp

    class _ListFindings(SecurityCenterRestStub):
        def __hash__(self):
            return hash("ListFindings")

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
            request: securitycenter_service.ListFindingsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> securitycenter_service.ListFindingsResponse:
            r"""Call the list findings method over HTTP.

            Args:
                request (~.securitycenter_service.ListFindingsRequest):
                    The request object. Request message for listing findings.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.securitycenter_service.ListFindingsResponse:
                    Response message for listing
                findings.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v2/{parent=organizations/*/sources/*}/findings",
                },
                {
                    "method": "get",
                    "uri": "/v2/{parent=organizations/*/sources/*/locations/*}/findings",
                },
                {
                    "method": "get",
                    "uri": "/v2/{parent=folders/*/sources/*}/findings",
                },
                {
                    "method": "get",
                    "uri": "/v2/{parent=folders/*/sources/*/locations/*}/findings",
                },
                {
                    "method": "get",
                    "uri": "/v2/{parent=projects/*/sources/*}/findings",
                },
                {
                    "method": "get",
                    "uri": "/v2/{parent=projects/*/sources/*/locations/*}/findings",
                },
            ]
            request, metadata = self._interceptor.pre_list_findings(request, metadata)
            pb_request = securitycenter_service.ListFindingsRequest.pb(request)
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
            resp = securitycenter_service.ListFindingsResponse()
            pb_resp = securitycenter_service.ListFindingsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_findings(resp)
            return resp

    class _ListMuteConfigs(SecurityCenterRestStub):
        def __hash__(self):
            return hash("ListMuteConfigs")

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
            request: securitycenter_service.ListMuteConfigsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> securitycenter_service.ListMuteConfigsResponse:
            r"""Call the list mute configs method over HTTP.

            Args:
                request (~.securitycenter_service.ListMuteConfigsRequest):
                    The request object. Request message for listing  mute
                configs at a given scope e.g.
                organization, folder or project. If no
                location is specified, default is
                global.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.securitycenter_service.ListMuteConfigsResponse:
                    Response message for listing mute
                configs.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v2/{parent=organizations/*}/muteConfigs",
                },
                {
                    "method": "get",
                    "uri": "/v2/{parent=organizations/*/locations/*}/muteConfigs",
                },
                {
                    "method": "get",
                    "uri": "/v2/{parent=folders/*}/muteConfigs",
                },
                {
                    "method": "get",
                    "uri": "/v2/{parent=folders/*/locations/*}/muteConfigs",
                },
                {
                    "method": "get",
                    "uri": "/v2/{parent=projects/*}/muteConfigs",
                },
                {
                    "method": "get",
                    "uri": "/v2/{parent=projects/*/locations/*}/muteConfigs",
                },
            ]
            request, metadata = self._interceptor.pre_list_mute_configs(
                request, metadata
            )
            pb_request = securitycenter_service.ListMuteConfigsRequest.pb(request)
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
            resp = securitycenter_service.ListMuteConfigsResponse()
            pb_resp = securitycenter_service.ListMuteConfigsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_mute_configs(resp)
            return resp

    class _ListNotificationConfigs(SecurityCenterRestStub):
        def __hash__(self):
            return hash("ListNotificationConfigs")

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
            request: securitycenter_service.ListNotificationConfigsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> securitycenter_service.ListNotificationConfigsResponse:
            r"""Call the list notification configs method over HTTP.

            Args:
                request (~.securitycenter_service.ListNotificationConfigsRequest):
                    The request object. Request message for listing
                notification configs.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.securitycenter_service.ListNotificationConfigsResponse:
                    Response message for listing
                notification configs.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v2/{parent=organizations/*/locations/*}/notificationConfigs",
                },
                {
                    "method": "get",
                    "uri": "/v2/{parent=folders/*/locations/*}/notificationConfigs",
                },
                {
                    "method": "get",
                    "uri": "/v2/{parent=projects/*/locations/*}/notificationConfigs",
                },
            ]
            request, metadata = self._interceptor.pre_list_notification_configs(
                request, metadata
            )
            pb_request = securitycenter_service.ListNotificationConfigsRequest.pb(
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
            resp = securitycenter_service.ListNotificationConfigsResponse()
            pb_resp = securitycenter_service.ListNotificationConfigsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_notification_configs(resp)
            return resp

    class _ListResourceValueConfigs(SecurityCenterRestStub):
        def __hash__(self):
            return hash("ListResourceValueConfigs")

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
            request: securitycenter_service.ListResourceValueConfigsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> securitycenter_service.ListResourceValueConfigsResponse:
            r"""Call the list resource value
            configs method over HTTP.

                Args:
                    request (~.securitycenter_service.ListResourceValueConfigsRequest):
                        The request object. Request message to list resource
                    value configs of a parent
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.securitycenter_service.ListResourceValueConfigsResponse:
                        Response message to list resource
                    value configs

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v2/{parent=organizations/*}/resourceValueConfigs",
                },
                {
                    "method": "get",
                    "uri": "/v2/{parent=organizations/*/locations/*}/resourceValueConfigs",
                },
            ]
            request, metadata = self._interceptor.pre_list_resource_value_configs(
                request, metadata
            )
            pb_request = securitycenter_service.ListResourceValueConfigsRequest.pb(
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
            resp = securitycenter_service.ListResourceValueConfigsResponse()
            pb_resp = securitycenter_service.ListResourceValueConfigsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_resource_value_configs(resp)
            return resp

    class _ListSources(SecurityCenterRestStub):
        def __hash__(self):
            return hash("ListSources")

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
            request: securitycenter_service.ListSourcesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> securitycenter_service.ListSourcesResponse:
            r"""Call the list sources method over HTTP.

            Args:
                request (~.securitycenter_service.ListSourcesRequest):
                    The request object. Request message for listing sources.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.securitycenter_service.ListSourcesResponse:
                    Response message for listing sources.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v2/{parent=organizations/*}/sources",
                },
                {
                    "method": "get",
                    "uri": "/v2/{parent=folders/*}/sources",
                },
                {
                    "method": "get",
                    "uri": "/v2/{parent=projects/*}/sources",
                },
            ]
            request, metadata = self._interceptor.pre_list_sources(request, metadata)
            pb_request = securitycenter_service.ListSourcesRequest.pb(request)
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
            resp = securitycenter_service.ListSourcesResponse()
            pb_resp = securitycenter_service.ListSourcesResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_sources(resp)
            return resp

    class _ListValuedResources(SecurityCenterRestStub):
        def __hash__(self):
            return hash("ListValuedResources")

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
            request: securitycenter_service.ListValuedResourcesRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> securitycenter_service.ListValuedResourcesResponse:
            r"""Call the list valued resources method over HTTP.

            Args:
                request (~.securitycenter_service.ListValuedResourcesRequest):
                    The request object. Request message for listing the
                valued resources for a given simulation.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.securitycenter_service.ListValuedResourcesResponse:
                    Response message for listing the
                valued resources for a given simulation.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v2/{parent=organizations/*/simulations/*}/valuedResources",
                },
                {
                    "method": "get",
                    "uri": "/v2/{parent=organizations/*/simulations/*/attackExposureResults/*}/valuedResources",
                },
            ]
            request, metadata = self._interceptor.pre_list_valued_resources(
                request, metadata
            )
            pb_request = securitycenter_service.ListValuedResourcesRequest.pb(request)
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
            resp = securitycenter_service.ListValuedResourcesResponse()
            pb_resp = securitycenter_service.ListValuedResourcesResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_valued_resources(resp)
            return resp

    class _SetFindingState(SecurityCenterRestStub):
        def __hash__(self):
            return hash("SetFindingState")

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
            request: securitycenter_service.SetFindingStateRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> finding.Finding:
            r"""Call the set finding state method over HTTP.

            Args:
                request (~.securitycenter_service.SetFindingStateRequest):
                    The request object. Request message for updating a
                finding's state.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.finding.Finding:
                    Security Command Center finding.

                A finding is a record of assessment data
                like security, risk, health, or privacy,
                that is ingested into Security Command
                Center for presentation, notification,
                analysis, policy testing, and
                enforcement. For example, a cross-site
                scripting (XSS) vulnerability in an App
                Engine application is a finding.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v2/{name=organizations/*/sources/*/findings/*}:setState",
                    "body": "*",
                },
                {
                    "method": "post",
                    "uri": "/v2/{name=organizations/*/sources/*/locations/*/findings/*}:setState",
                    "body": "*",
                },
                {
                    "method": "post",
                    "uri": "/v2/{name=folders/*/sources/*/findings/*}:setState",
                    "body": "*",
                },
                {
                    "method": "post",
                    "uri": "/v2/{name=folders/*/sources/*/locations/*/findings/*}:setState",
                    "body": "*",
                },
                {
                    "method": "post",
                    "uri": "/v2/{name=projects/*/sources/*/findings/*}:setState",
                    "body": "*",
                },
                {
                    "method": "post",
                    "uri": "/v2/{name=projects/*/sources/*/locations/*/findings/*}:setState",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_set_finding_state(
                request, metadata
            )
            pb_request = securitycenter_service.SetFindingStateRequest.pb(request)
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
            resp = finding.Finding()
            pb_resp = finding.Finding.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_set_finding_state(resp)
            return resp

    class _SetIamPolicy(SecurityCenterRestStub):
        def __hash__(self):
            return hash("SetIamPolicy")

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
            request: iam_policy_pb2.SetIamPolicyRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> policy_pb2.Policy:
            r"""Call the set iam policy method over HTTP.

            Args:
                request (~.iam_policy_pb2.SetIamPolicyRequest):
                    The request object. Request message for ``SetIamPolicy`` method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

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

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v2/{resource=organizations/*/sources/*}:setIamPolicy",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_set_iam_policy(request, metadata)
            pb_request = request
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
            resp = policy_pb2.Policy()
            pb_resp = resp

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_set_iam_policy(resp)
            return resp

    class _SetMute(SecurityCenterRestStub):
        def __hash__(self):
            return hash("SetMute")

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
            request: securitycenter_service.SetMuteRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> finding.Finding:
            r"""Call the set mute method over HTTP.

            Args:
                request (~.securitycenter_service.SetMuteRequest):
                    The request object. Request message for updating a
                finding's mute status.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.finding.Finding:
                    Security Command Center finding.

                A finding is a record of assessment data
                like security, risk, health, or privacy,
                that is ingested into Security Command
                Center for presentation, notification,
                analysis, policy testing, and
                enforcement. For example, a cross-site
                scripting (XSS) vulnerability in an App
                Engine application is a finding.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v2/{name=organizations/*/sources/*/findings/*}:setMute",
                    "body": "*",
                },
                {
                    "method": "post",
                    "uri": "/v2/{name=organizations/*/sources/*/locations/*/findings/*}:setMute",
                    "body": "*",
                },
                {
                    "method": "post",
                    "uri": "/v2/{name=folders/*/sources/*/findings/*}:setMute",
                    "body": "*",
                },
                {
                    "method": "post",
                    "uri": "/v2/{name=folders/*/sources/*/locations/*/findings/*}:setMute",
                    "body": "*",
                },
                {
                    "method": "post",
                    "uri": "/v2/{name=projects/*/sources/*/findings/*}:setMute",
                    "body": "*",
                },
                {
                    "method": "post",
                    "uri": "/v2/{name=projects/*/sources/*/locations/*/findings/*}:setMute",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_set_mute(request, metadata)
            pb_request = securitycenter_service.SetMuteRequest.pb(request)
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
            resp = finding.Finding()
            pb_resp = finding.Finding.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_set_mute(resp)
            return resp

    class _TestIamPermissions(SecurityCenterRestStub):
        def __hash__(self):
            return hash("TestIamPermissions")

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
            request: iam_policy_pb2.TestIamPermissionsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> iam_policy_pb2.TestIamPermissionsResponse:
            r"""Call the test iam permissions method over HTTP.

            Args:
                request (~.iam_policy_pb2.TestIamPermissionsRequest):
                    The request object. Request message for ``TestIamPermissions`` method.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.iam_policy_pb2.TestIamPermissionsResponse:
                    Response message for ``TestIamPermissions`` method.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v2/{resource=organizations/*/sources/*}:testIamPermissions",
                    "body": "*",
                },
            ]
            request, metadata = self._interceptor.pre_test_iam_permissions(
                request, metadata
            )
            pb_request = request
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
            resp = iam_policy_pb2.TestIamPermissionsResponse()
            pb_resp = resp

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_test_iam_permissions(resp)
            return resp

    class _UpdateBigQueryExport(SecurityCenterRestStub):
        def __hash__(self):
            return hash("UpdateBigQueryExport")

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
            request: securitycenter_service.UpdateBigQueryExportRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> bigquery_export.BigQueryExport:
            r"""Call the update big query export method over HTTP.

            Args:
                request (~.securitycenter_service.UpdateBigQueryExportRequest):
                    The request object. Request message for updating a
                BigQuery export.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.bigquery_export.BigQueryExport:
                    Configures how to deliver Findings to
                BigQuery Instance.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "patch",
                    "uri": "/v2/{big_query_export.name=organizations/*/locations/*/bigQueryExports/*}",
                    "body": "big_query_export",
                },
                {
                    "method": "patch",
                    "uri": "/v2/{big_query_export.name=folders/*/locations/*/bigQueryExports/*}",
                    "body": "big_query_export",
                },
                {
                    "method": "patch",
                    "uri": "/v2/{big_query_export.name=projects/*/locations/*/bigQueryExports/*}",
                    "body": "big_query_export",
                },
            ]
            request, metadata = self._interceptor.pre_update_big_query_export(
                request, metadata
            )
            pb_request = securitycenter_service.UpdateBigQueryExportRequest.pb(request)
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
            resp = bigquery_export.BigQueryExport()
            pb_resp = bigquery_export.BigQueryExport.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_big_query_export(resp)
            return resp

    class _UpdateExternalSystem(SecurityCenterRestStub):
        def __hash__(self):
            return hash("UpdateExternalSystem")

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
            request: securitycenter_service.UpdateExternalSystemRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> gcs_external_system.ExternalSystem:
            r"""Call the update external system method over HTTP.

            Args:
                request (~.securitycenter_service.UpdateExternalSystemRequest):
                    The request object. Request message for updating a
                ExternalSystem resource.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.gcs_external_system.ExternalSystem:
                    Representation of third party
                SIEM/SOAR fields within SCC.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "patch",
                    "uri": "/v2/{external_system.name=organizations/*/sources/*/findings/*/externalSystems/*}",
                    "body": "external_system",
                },
                {
                    "method": "patch",
                    "uri": "/v2/{external_system.name=organizations/*/sources/*/locations/*/findings/*/externalSystems/*}",
                    "body": "external_system",
                },
                {
                    "method": "patch",
                    "uri": "/v2/{external_system.name=folders/*/sources/*/findings/*/externalSystems/*}",
                    "body": "external_system",
                },
                {
                    "method": "patch",
                    "uri": "/v2/{external_system.name=folders/*/sources/*/locations/*/findings/*/externalSystems/*}",
                    "body": "external_system",
                },
                {
                    "method": "patch",
                    "uri": "/v2/{external_system.name=projects/*/sources/*/findings/*/externalSystems/*}",
                    "body": "external_system",
                },
                {
                    "method": "patch",
                    "uri": "/v2/{external_system.name=projects/*/sources/*/locations/*/findings/*/externalSystems/*}",
                    "body": "external_system",
                },
            ]
            request, metadata = self._interceptor.pre_update_external_system(
                request, metadata
            )
            pb_request = securitycenter_service.UpdateExternalSystemRequest.pb(request)
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
            resp = gcs_external_system.ExternalSystem()
            pb_resp = gcs_external_system.ExternalSystem.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_external_system(resp)
            return resp

    class _UpdateFinding(SecurityCenterRestStub):
        def __hash__(self):
            return hash("UpdateFinding")

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
            request: securitycenter_service.UpdateFindingRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> gcs_finding.Finding:
            r"""Call the update finding method over HTTP.

            Args:
                request (~.securitycenter_service.UpdateFindingRequest):
                    The request object. Request message for updating or
                creating a finding.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.gcs_finding.Finding:
                    Security Command Center finding.

                A finding is a record of assessment data
                like security, risk, health, or privacy,
                that is ingested into Security Command
                Center for presentation, notification,
                analysis, policy testing, and
                enforcement. For example, a cross-site
                scripting (XSS) vulnerability in an App
                Engine application is a finding.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "patch",
                    "uri": "/v2/{finding.name=organizations/*/sources/*/findings/*}",
                    "body": "finding",
                },
                {
                    "method": "patch",
                    "uri": "/v2/{finding.name=organizations/*/sources/*/locations/*/findings/*}",
                    "body": "finding",
                },
                {
                    "method": "patch",
                    "uri": "/v2/{finding.name=folders/*/sources/*/findings/*}",
                    "body": "finding",
                },
                {
                    "method": "patch",
                    "uri": "/v2/{finding.name=folders/*/sources/*/locations/*/findings/*}",
                    "body": "finding",
                },
                {
                    "method": "patch",
                    "uri": "/v2/{finding.name=projects/*/sources/*/findings/*}",
                    "body": "finding",
                },
                {
                    "method": "patch",
                    "uri": "/v2/{finding.name=projects/*/sources/*/locations/*/findings/*}",
                    "body": "finding",
                },
            ]
            request, metadata = self._interceptor.pre_update_finding(request, metadata)
            pb_request = securitycenter_service.UpdateFindingRequest.pb(request)
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
            resp = gcs_finding.Finding()
            pb_resp = gcs_finding.Finding.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_finding(resp)
            return resp

    class _UpdateMuteConfig(SecurityCenterRestStub):
        def __hash__(self):
            return hash("UpdateMuteConfig")

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
            request: securitycenter_service.UpdateMuteConfigRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> gcs_mute_config.MuteConfig:
            r"""Call the update mute config method over HTTP.

            Args:
                request (~.securitycenter_service.UpdateMuteConfigRequest):
                    The request object. Request message for updating a mute
                config.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.gcs_mute_config.MuteConfig:
                    A mute config is a Cloud SCC resource
                that contains the configuration to mute
                create/update events of findings.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "patch",
                    "uri": "/v2/{mute_config.name=organizations/*/muteConfigs/*}",
                    "body": "mute_config",
                },
                {
                    "method": "patch",
                    "uri": "/v2/{mute_config.name=organizations/*/locations/*/muteConfigs/*}",
                    "body": "mute_config",
                },
                {
                    "method": "patch",
                    "uri": "/v2/{mute_config.name=folders/*/muteConfigs/*}",
                    "body": "mute_config",
                },
                {
                    "method": "patch",
                    "uri": "/v2/{mute_config.name=folders/*/locations/*/muteConfigs/*}",
                    "body": "mute_config",
                },
                {
                    "method": "patch",
                    "uri": "/v2/{mute_config.name=projects/*/muteConfigs/*}",
                    "body": "mute_config",
                },
                {
                    "method": "patch",
                    "uri": "/v2/{mute_config.name=projects/*/locations/*/muteConfigs/*}",
                    "body": "mute_config",
                },
            ]
            request, metadata = self._interceptor.pre_update_mute_config(
                request, metadata
            )
            pb_request = securitycenter_service.UpdateMuteConfigRequest.pb(request)
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
            resp = gcs_mute_config.MuteConfig()
            pb_resp = gcs_mute_config.MuteConfig.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_mute_config(resp)
            return resp

    class _UpdateNotificationConfig(SecurityCenterRestStub):
        def __hash__(self):
            return hash("UpdateNotificationConfig")

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
            request: securitycenter_service.UpdateNotificationConfigRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> gcs_notification_config.NotificationConfig:
            r"""Call the update notification
            config method over HTTP.

                Args:
                    request (~.securitycenter_service.UpdateNotificationConfigRequest):
                        The request object. Request message for updating a
                    notification config.
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.gcs_notification_config.NotificationConfig:
                        Cloud Security Command Center (Cloud
                    SCC) notification configs.
                    A notification config is a Cloud SCC
                    resource that contains the configuration
                    to send notifications for create/update
                    events of findings, assets and etc.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "patch",
                    "uri": "/v2/{notification_config.name=organizations/*/locations/*/notificationConfigs/*}",
                    "body": "notification_config",
                },
                {
                    "method": "patch",
                    "uri": "/v2/{notification_config.name=folders/*/locations/*/notificationConfigs/*}",
                    "body": "notification_config",
                },
                {
                    "method": "patch",
                    "uri": "/v2/{notification_config.name=projects/*/locations/*/notificationConfigs/*}",
                    "body": "notification_config",
                },
            ]
            request, metadata = self._interceptor.pre_update_notification_config(
                request, metadata
            )
            pb_request = securitycenter_service.UpdateNotificationConfigRequest.pb(
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
            resp = gcs_notification_config.NotificationConfig()
            pb_resp = gcs_notification_config.NotificationConfig.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_notification_config(resp)
            return resp

    class _UpdateResourceValueConfig(SecurityCenterRestStub):
        def __hash__(self):
            return hash("UpdateResourceValueConfig")

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
            request: securitycenter_service.UpdateResourceValueConfigRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> gcs_resource_value_config.ResourceValueConfig:
            r"""Call the update resource value
            config method over HTTP.

                Args:
                    request (~.securitycenter_service.UpdateResourceValueConfigRequest):
                        The request object. Request message to update resource
                    value config
                    retry (google.api_core.retry.Retry): Designation of what errors, if any,
                        should be retried.
                    timeout (float): The timeout for this request.
                    metadata (Sequence[Tuple[str, str]]): Strings which should be
                        sent along with the request as metadata.

                Returns:
                    ~.gcs_resource_value_config.ResourceValueConfig:
                        A resource value configuration (RVC)
                    is a mapping configuration of user's
                    resources to resource values. Used in
                    Attack path simulations.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "patch",
                    "uri": "/v2/{resource_value_config.name=organizations/*/resourceValueConfigs/*}",
                    "body": "resource_value_config",
                },
                {
                    "method": "patch",
                    "uri": "/v2/{resource_value_config.name=organizations/*/locations/*/resourceValueConfigs/*}",
                    "body": "resource_value_config",
                },
            ]
            request, metadata = self._interceptor.pre_update_resource_value_config(
                request, metadata
            )
            pb_request = securitycenter_service.UpdateResourceValueConfigRequest.pb(
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
            resp = gcs_resource_value_config.ResourceValueConfig()
            pb_resp = gcs_resource_value_config.ResourceValueConfig.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_resource_value_config(resp)
            return resp

    class _UpdateSecurityMarks(SecurityCenterRestStub):
        def __hash__(self):
            return hash("UpdateSecurityMarks")

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
            request: securitycenter_service.UpdateSecurityMarksRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> gcs_security_marks.SecurityMarks:
            r"""Call the update security marks method over HTTP.

            Args:
                request (~.securitycenter_service.UpdateSecurityMarksRequest):
                    The request object. Request message for updating a
                SecurityMarks resource.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.gcs_security_marks.SecurityMarks:
                    User specified security marks that
                are attached to the parent Security
                Command Center resource. Security marks
                are scoped within a Security Command
                Center organization -- they can be
                modified and viewed by all users who
                have proper permissions on the
                organization.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "patch",
                    "uri": "/v2/{security_marks.name=organizations/*/sources/*/findings/*/securityMarks}",
                    "body": "security_marks",
                },
                {
                    "method": "patch",
                    "uri": "/v2/{security_marks.name=organizations/*/assets/*/securityMarks}",
                    "body": "security_marks",
                },
                {
                    "method": "patch",
                    "uri": "/v2/{security_marks.name=organizations/*/sources/*/locations/*/findings/*/securityMarks}",
                    "body": "security_marks",
                },
                {
                    "method": "patch",
                    "uri": "/v2/{security_marks.name=folders/*/sources/*/findings/*/securityMarks}",
                    "body": "security_marks",
                },
                {
                    "method": "patch",
                    "uri": "/v2/{security_marks.name=folders/*/assets/*/securityMarks}",
                    "body": "security_marks",
                },
                {
                    "method": "patch",
                    "uri": "/v2/{security_marks.name=folders/*/sources/*/locations/*/findings/*/securityMarks}",
                    "body": "security_marks",
                },
                {
                    "method": "patch",
                    "uri": "/v2/{security_marks.name=projects/*/sources/*/findings/*/securityMarks}",
                    "body": "security_marks",
                },
                {
                    "method": "patch",
                    "uri": "/v2/{security_marks.name=projects/*/assets/*/securityMarks}",
                    "body": "security_marks",
                },
                {
                    "method": "patch",
                    "uri": "/v2/{security_marks.name=projects/*/sources/*/locations/*/findings/*/securityMarks}",
                    "body": "security_marks",
                },
            ]
            request, metadata = self._interceptor.pre_update_security_marks(
                request, metadata
            )
            pb_request = securitycenter_service.UpdateSecurityMarksRequest.pb(request)
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
            resp = gcs_security_marks.SecurityMarks()
            pb_resp = gcs_security_marks.SecurityMarks.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_security_marks(resp)
            return resp

    class _UpdateSource(SecurityCenterRestStub):
        def __hash__(self):
            return hash("UpdateSource")

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
            request: securitycenter_service.UpdateSourceRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: Optional[float] = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> gcs_source.Source:
            r"""Call the update source method over HTTP.

            Args:
                request (~.securitycenter_service.UpdateSourceRequest):
                    The request object. Request message for updating a
                source.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.gcs_source.Source:
                    Security Command Center finding
                source. A finding source is an entity or
                a mechanism that can produce a finding.
                A source is like a container of findings
                that come from the same scanner, logger,
                monitor, and other tools.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "patch",
                    "uri": "/v2/{source.name=organizations/*/sources/*}",
                    "body": "source",
                },
            ]
            request, metadata = self._interceptor.pre_update_source(request, metadata)
            pb_request = securitycenter_service.UpdateSourceRequest.pb(request)
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
            resp = gcs_source.Source()
            pb_resp = gcs_source.Source.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_source(resp)
            return resp

    @property
    def batch_create_resource_value_configs(
        self,
    ) -> Callable[
        [securitycenter_service.BatchCreateResourceValueConfigsRequest],
        securitycenter_service.BatchCreateResourceValueConfigsResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._BatchCreateResourceValueConfigs(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def bulk_mute_findings(
        self,
    ) -> Callable[
        [securitycenter_service.BulkMuteFindingsRequest], operations_pb2.Operation
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._BulkMuteFindings(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_big_query_export(
        self,
    ) -> Callable[
        [securitycenter_service.CreateBigQueryExportRequest],
        bigquery_export.BigQueryExport,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateBigQueryExport(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_finding(
        self,
    ) -> Callable[[securitycenter_service.CreateFindingRequest], gcs_finding.Finding]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateFinding(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_mute_config(
        self,
    ) -> Callable[
        [securitycenter_service.CreateMuteConfigRequest], gcs_mute_config.MuteConfig
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateMuteConfig(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_notification_config(
        self,
    ) -> Callable[
        [securitycenter_service.CreateNotificationConfigRequest],
        gcs_notification_config.NotificationConfig,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateNotificationConfig(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_source(
        self,
    ) -> Callable[[securitycenter_service.CreateSourceRequest], gcs_source.Source]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateSource(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_big_query_export(
        self,
    ) -> Callable[
        [securitycenter_service.DeleteBigQueryExportRequest], empty_pb2.Empty
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteBigQueryExport(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_mute_config(
        self,
    ) -> Callable[[securitycenter_service.DeleteMuteConfigRequest], empty_pb2.Empty]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteMuteConfig(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_notification_config(
        self,
    ) -> Callable[
        [securitycenter_service.DeleteNotificationConfigRequest], empty_pb2.Empty
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteNotificationConfig(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_resource_value_config(
        self,
    ) -> Callable[
        [securitycenter_service.DeleteResourceValueConfigRequest], empty_pb2.Empty
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteResourceValueConfig(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_big_query_export(
        self,
    ) -> Callable[
        [securitycenter_service.GetBigQueryExportRequest],
        bigquery_export.BigQueryExport,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetBigQueryExport(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_iam_policy(
        self,
    ) -> Callable[[iam_policy_pb2.GetIamPolicyRequest], policy_pb2.Policy]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetIamPolicy(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_mute_config(
        self,
    ) -> Callable[
        [securitycenter_service.GetMuteConfigRequest], mute_config.MuteConfig
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetMuteConfig(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_notification_config(
        self,
    ) -> Callable[
        [securitycenter_service.GetNotificationConfigRequest],
        notification_config.NotificationConfig,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetNotificationConfig(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_resource_value_config(
        self,
    ) -> Callable[
        [securitycenter_service.GetResourceValueConfigRequest],
        resource_value_config.ResourceValueConfig,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetResourceValueConfig(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_simulation(
        self,
    ) -> Callable[[securitycenter_service.GetSimulationRequest], simulation.Simulation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetSimulation(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_source(
        self,
    ) -> Callable[[securitycenter_service.GetSourceRequest], source.Source]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetSource(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_valued_resource(
        self,
    ) -> Callable[
        [securitycenter_service.GetValuedResourceRequest],
        valued_resource.ValuedResource,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetValuedResource(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def group_findings(
        self,
    ) -> Callable[
        [securitycenter_service.GroupFindingsRequest],
        securitycenter_service.GroupFindingsResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GroupFindings(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_attack_paths(
        self,
    ) -> Callable[
        [securitycenter_service.ListAttackPathsRequest],
        securitycenter_service.ListAttackPathsResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListAttackPaths(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_big_query_exports(
        self,
    ) -> Callable[
        [securitycenter_service.ListBigQueryExportsRequest],
        securitycenter_service.ListBigQueryExportsResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListBigQueryExports(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_findings(
        self,
    ) -> Callable[
        [securitycenter_service.ListFindingsRequest],
        securitycenter_service.ListFindingsResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListFindings(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_mute_configs(
        self,
    ) -> Callable[
        [securitycenter_service.ListMuteConfigsRequest],
        securitycenter_service.ListMuteConfigsResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListMuteConfigs(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_notification_configs(
        self,
    ) -> Callable[
        [securitycenter_service.ListNotificationConfigsRequest],
        securitycenter_service.ListNotificationConfigsResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListNotificationConfigs(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_resource_value_configs(
        self,
    ) -> Callable[
        [securitycenter_service.ListResourceValueConfigsRequest],
        securitycenter_service.ListResourceValueConfigsResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListResourceValueConfigs(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_sources(
        self,
    ) -> Callable[
        [securitycenter_service.ListSourcesRequest],
        securitycenter_service.ListSourcesResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListSources(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_valued_resources(
        self,
    ) -> Callable[
        [securitycenter_service.ListValuedResourcesRequest],
        securitycenter_service.ListValuedResourcesResponse,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListValuedResources(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def set_finding_state(
        self,
    ) -> Callable[[securitycenter_service.SetFindingStateRequest], finding.Finding]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._SetFindingState(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def set_iam_policy(
        self,
    ) -> Callable[[iam_policy_pb2.SetIamPolicyRequest], policy_pb2.Policy]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._SetIamPolicy(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def set_mute(
        self,
    ) -> Callable[[securitycenter_service.SetMuteRequest], finding.Finding]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._SetMute(self._session, self._host, self._interceptor)  # type: ignore

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
    def update_big_query_export(
        self,
    ) -> Callable[
        [securitycenter_service.UpdateBigQueryExportRequest],
        bigquery_export.BigQueryExport,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateBigQueryExport(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_external_system(
        self,
    ) -> Callable[
        [securitycenter_service.UpdateExternalSystemRequest],
        gcs_external_system.ExternalSystem,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateExternalSystem(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_finding(
        self,
    ) -> Callable[[securitycenter_service.UpdateFindingRequest], gcs_finding.Finding]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateFinding(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_mute_config(
        self,
    ) -> Callable[
        [securitycenter_service.UpdateMuteConfigRequest], gcs_mute_config.MuteConfig
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateMuteConfig(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_notification_config(
        self,
    ) -> Callable[
        [securitycenter_service.UpdateNotificationConfigRequest],
        gcs_notification_config.NotificationConfig,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateNotificationConfig(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_resource_value_config(
        self,
    ) -> Callable[
        [securitycenter_service.UpdateResourceValueConfigRequest],
        gcs_resource_value_config.ResourceValueConfig,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateResourceValueConfig(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_security_marks(
        self,
    ) -> Callable[
        [securitycenter_service.UpdateSecurityMarksRequest],
        gcs_security_marks.SecurityMarks,
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateSecurityMarks(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_source(
        self,
    ) -> Callable[[securitycenter_service.UpdateSourceRequest], gcs_source.Source]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateSource(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def cancel_operation(self):
        return self._CancelOperation(self._session, self._host, self._interceptor)  # type: ignore

    class _CancelOperation(SecurityCenterRestStub):
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
                    "uri": "/v2/{name=organizations/*/operations/*}:cancel",
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

    class _DeleteOperation(SecurityCenterRestStub):
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
                    "uri": "/v2/{name=organizations/*/operations/*}",
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

    class _GetOperation(SecurityCenterRestStub):
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
                    "uri": "/v2/{name=organizations/*/operations/*}",
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

    class _ListOperations(SecurityCenterRestStub):
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
                    "uri": "/v2/{name=organizations/*/operations}",
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


__all__ = ("SecurityCenterRestTransport",)
