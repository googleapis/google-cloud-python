# -*- coding: utf-8 -*-
# Copyright 2023 Google LLC
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
from google.cloud.monitoring import gapic_version as package_version

__version__ = package_version.__version__


from google.cloud.monitoring_v3.services.alert_policy_service.client import (
    AlertPolicyServiceClient,
)
from google.cloud.monitoring_v3.services.alert_policy_service.async_client import (
    AlertPolicyServiceAsyncClient,
)
from google.cloud.monitoring_v3.services.group_service.client import GroupServiceClient
from google.cloud.monitoring_v3.services.group_service.async_client import (
    GroupServiceAsyncClient,
)
from google.cloud.monitoring_v3.services.metric_service.client import (
    MetricServiceClient,
)
from google.cloud.monitoring_v3.services.metric_service.async_client import (
    MetricServiceAsyncClient,
)
from google.cloud.monitoring_v3.services.notification_channel_service.client import (
    NotificationChannelServiceClient,
)
from google.cloud.monitoring_v3.services.notification_channel_service.async_client import (
    NotificationChannelServiceAsyncClient,
)
from google.cloud.monitoring_v3.services.query_service.client import QueryServiceClient
from google.cloud.monitoring_v3.services.query_service.async_client import (
    QueryServiceAsyncClient,
)
from google.cloud.monitoring_v3.services.service_monitoring_service.client import (
    ServiceMonitoringServiceClient,
)
from google.cloud.monitoring_v3.services.service_monitoring_service.async_client import (
    ServiceMonitoringServiceAsyncClient,
)
from google.cloud.monitoring_v3.services.snooze_service.client import (
    SnoozeServiceClient,
)
from google.cloud.monitoring_v3.services.snooze_service.async_client import (
    SnoozeServiceAsyncClient,
)
from google.cloud.monitoring_v3.services.uptime_check_service.client import (
    UptimeCheckServiceClient,
)
from google.cloud.monitoring_v3.services.uptime_check_service.async_client import (
    UptimeCheckServiceAsyncClient,
)

from google.cloud.monitoring_v3.types.alert import AlertPolicy
from google.cloud.monitoring_v3.types.alert_service import CreateAlertPolicyRequest
from google.cloud.monitoring_v3.types.alert_service import DeleteAlertPolicyRequest
from google.cloud.monitoring_v3.types.alert_service import GetAlertPolicyRequest
from google.cloud.monitoring_v3.types.alert_service import ListAlertPoliciesRequest
from google.cloud.monitoring_v3.types.alert_service import ListAlertPoliciesResponse
from google.cloud.monitoring_v3.types.alert_service import UpdateAlertPolicyRequest
from google.cloud.monitoring_v3.types.common import Aggregation
from google.cloud.monitoring_v3.types.common import TimeInterval
from google.cloud.monitoring_v3.types.common import TypedValue
from google.cloud.monitoring_v3.types.common import ComparisonType
from google.cloud.monitoring_v3.types.common import ServiceTier
from google.cloud.monitoring_v3.types.dropped_labels import DroppedLabels
from google.cloud.monitoring_v3.types.group import Group
from google.cloud.monitoring_v3.types.group_service import CreateGroupRequest
from google.cloud.monitoring_v3.types.group_service import DeleteGroupRequest
from google.cloud.monitoring_v3.types.group_service import GetGroupRequest
from google.cloud.monitoring_v3.types.group_service import ListGroupMembersRequest
from google.cloud.monitoring_v3.types.group_service import ListGroupMembersResponse
from google.cloud.monitoring_v3.types.group_service import ListGroupsRequest
from google.cloud.monitoring_v3.types.group_service import ListGroupsResponse
from google.cloud.monitoring_v3.types.group_service import UpdateGroupRequest
from google.cloud.monitoring_v3.types.metric import LabelValue
from google.cloud.monitoring_v3.types.metric import Point
from google.cloud.monitoring_v3.types.metric import QueryError
from google.cloud.monitoring_v3.types.metric import TextLocator
from google.cloud.monitoring_v3.types.metric import TimeSeries
from google.cloud.monitoring_v3.types.metric import TimeSeriesData
from google.cloud.monitoring_v3.types.metric import TimeSeriesDescriptor
from google.cloud.monitoring_v3.types.metric_service import (
    CreateMetricDescriptorRequest,
)
from google.cloud.monitoring_v3.types.metric_service import CreateTimeSeriesError
from google.cloud.monitoring_v3.types.metric_service import CreateTimeSeriesRequest
from google.cloud.monitoring_v3.types.metric_service import CreateTimeSeriesSummary
from google.cloud.monitoring_v3.types.metric_service import (
    DeleteMetricDescriptorRequest,
)
from google.cloud.monitoring_v3.types.metric_service import GetMetricDescriptorRequest
from google.cloud.monitoring_v3.types.metric_service import (
    GetMonitoredResourceDescriptorRequest,
)
from google.cloud.monitoring_v3.types.metric_service import ListMetricDescriptorsRequest
from google.cloud.monitoring_v3.types.metric_service import (
    ListMetricDescriptorsResponse,
)
from google.cloud.monitoring_v3.types.metric_service import (
    ListMonitoredResourceDescriptorsRequest,
)
from google.cloud.monitoring_v3.types.metric_service import (
    ListMonitoredResourceDescriptorsResponse,
)
from google.cloud.monitoring_v3.types.metric_service import ListTimeSeriesRequest
from google.cloud.monitoring_v3.types.metric_service import ListTimeSeriesResponse
from google.cloud.monitoring_v3.types.metric_service import QueryErrorList
from google.cloud.monitoring_v3.types.metric_service import QueryTimeSeriesRequest
from google.cloud.monitoring_v3.types.metric_service import QueryTimeSeriesResponse
from google.cloud.monitoring_v3.types.mutation_record import MutationRecord
from google.cloud.monitoring_v3.types.notification import NotificationChannel
from google.cloud.monitoring_v3.types.notification import NotificationChannelDescriptor
from google.cloud.monitoring_v3.types.notification_service import (
    CreateNotificationChannelRequest,
)
from google.cloud.monitoring_v3.types.notification_service import (
    DeleteNotificationChannelRequest,
)
from google.cloud.monitoring_v3.types.notification_service import (
    GetNotificationChannelDescriptorRequest,
)
from google.cloud.monitoring_v3.types.notification_service import (
    GetNotificationChannelRequest,
)
from google.cloud.monitoring_v3.types.notification_service import (
    GetNotificationChannelVerificationCodeRequest,
)
from google.cloud.monitoring_v3.types.notification_service import (
    GetNotificationChannelVerificationCodeResponse,
)
from google.cloud.monitoring_v3.types.notification_service import (
    ListNotificationChannelDescriptorsRequest,
)
from google.cloud.monitoring_v3.types.notification_service import (
    ListNotificationChannelDescriptorsResponse,
)
from google.cloud.monitoring_v3.types.notification_service import (
    ListNotificationChannelsRequest,
)
from google.cloud.monitoring_v3.types.notification_service import (
    ListNotificationChannelsResponse,
)
from google.cloud.monitoring_v3.types.notification_service import (
    SendNotificationChannelVerificationCodeRequest,
)
from google.cloud.monitoring_v3.types.notification_service import (
    UpdateNotificationChannelRequest,
)
from google.cloud.monitoring_v3.types.notification_service import (
    VerifyNotificationChannelRequest,
)
from google.cloud.monitoring_v3.types.service import BasicSli
from google.cloud.monitoring_v3.types.service import DistributionCut
from google.cloud.monitoring_v3.types.service import Range
from google.cloud.monitoring_v3.types.service import RequestBasedSli
from google.cloud.monitoring_v3.types.service import Service
from google.cloud.monitoring_v3.types.service import ServiceLevelIndicator
from google.cloud.monitoring_v3.types.service import ServiceLevelObjective
from google.cloud.monitoring_v3.types.service import TimeSeriesRatio
from google.cloud.monitoring_v3.types.service import WindowsBasedSli
from google.cloud.monitoring_v3.types.service_service import (
    CreateServiceLevelObjectiveRequest,
)
from google.cloud.monitoring_v3.types.service_service import CreateServiceRequest
from google.cloud.monitoring_v3.types.service_service import (
    DeleteServiceLevelObjectiveRequest,
)
from google.cloud.monitoring_v3.types.service_service import DeleteServiceRequest
from google.cloud.monitoring_v3.types.service_service import (
    GetServiceLevelObjectiveRequest,
)
from google.cloud.monitoring_v3.types.service_service import GetServiceRequest
from google.cloud.monitoring_v3.types.service_service import (
    ListServiceLevelObjectivesRequest,
)
from google.cloud.monitoring_v3.types.service_service import (
    ListServiceLevelObjectivesResponse,
)
from google.cloud.monitoring_v3.types.service_service import ListServicesRequest
from google.cloud.monitoring_v3.types.service_service import ListServicesResponse
from google.cloud.monitoring_v3.types.service_service import (
    UpdateServiceLevelObjectiveRequest,
)
from google.cloud.monitoring_v3.types.service_service import UpdateServiceRequest
from google.cloud.monitoring_v3.types.snooze import Snooze
from google.cloud.monitoring_v3.types.snooze_service import CreateSnoozeRequest
from google.cloud.monitoring_v3.types.snooze_service import GetSnoozeRequest
from google.cloud.monitoring_v3.types.snooze_service import ListSnoozesRequest
from google.cloud.monitoring_v3.types.snooze_service import ListSnoozesResponse
from google.cloud.monitoring_v3.types.snooze_service import UpdateSnoozeRequest
from google.cloud.monitoring_v3.types.span_context import SpanContext
from google.cloud.monitoring_v3.types.uptime import InternalChecker
from google.cloud.monitoring_v3.types.uptime import UptimeCheckConfig
from google.cloud.monitoring_v3.types.uptime import UptimeCheckIp
from google.cloud.monitoring_v3.types.uptime import GroupResourceType
from google.cloud.monitoring_v3.types.uptime import UptimeCheckRegion
from google.cloud.monitoring_v3.types.uptime_service import (
    CreateUptimeCheckConfigRequest,
)
from google.cloud.monitoring_v3.types.uptime_service import (
    DeleteUptimeCheckConfigRequest,
)
from google.cloud.monitoring_v3.types.uptime_service import GetUptimeCheckConfigRequest
from google.cloud.monitoring_v3.types.uptime_service import (
    ListUptimeCheckConfigsRequest,
)
from google.cloud.monitoring_v3.types.uptime_service import (
    ListUptimeCheckConfigsResponse,
)
from google.cloud.monitoring_v3.types.uptime_service import ListUptimeCheckIpsRequest
from google.cloud.monitoring_v3.types.uptime_service import ListUptimeCheckIpsResponse
from google.cloud.monitoring_v3.types.uptime_service import (
    UpdateUptimeCheckConfigRequest,
)

__all__ = (
    "AlertPolicyServiceClient",
    "AlertPolicyServiceAsyncClient",
    "GroupServiceClient",
    "GroupServiceAsyncClient",
    "MetricServiceClient",
    "MetricServiceAsyncClient",
    "NotificationChannelServiceClient",
    "NotificationChannelServiceAsyncClient",
    "QueryServiceClient",
    "QueryServiceAsyncClient",
    "ServiceMonitoringServiceClient",
    "ServiceMonitoringServiceAsyncClient",
    "SnoozeServiceClient",
    "SnoozeServiceAsyncClient",
    "UptimeCheckServiceClient",
    "UptimeCheckServiceAsyncClient",
    "AlertPolicy",
    "CreateAlertPolicyRequest",
    "DeleteAlertPolicyRequest",
    "GetAlertPolicyRequest",
    "ListAlertPoliciesRequest",
    "ListAlertPoliciesResponse",
    "UpdateAlertPolicyRequest",
    "Aggregation",
    "TimeInterval",
    "TypedValue",
    "ComparisonType",
    "ServiceTier",
    "DroppedLabels",
    "Group",
    "CreateGroupRequest",
    "DeleteGroupRequest",
    "GetGroupRequest",
    "ListGroupMembersRequest",
    "ListGroupMembersResponse",
    "ListGroupsRequest",
    "ListGroupsResponse",
    "UpdateGroupRequest",
    "LabelValue",
    "Point",
    "QueryError",
    "TextLocator",
    "TimeSeries",
    "TimeSeriesData",
    "TimeSeriesDescriptor",
    "CreateMetricDescriptorRequest",
    "CreateTimeSeriesError",
    "CreateTimeSeriesRequest",
    "CreateTimeSeriesSummary",
    "DeleteMetricDescriptorRequest",
    "GetMetricDescriptorRequest",
    "GetMonitoredResourceDescriptorRequest",
    "ListMetricDescriptorsRequest",
    "ListMetricDescriptorsResponse",
    "ListMonitoredResourceDescriptorsRequest",
    "ListMonitoredResourceDescriptorsResponse",
    "ListTimeSeriesRequest",
    "ListTimeSeriesResponse",
    "QueryErrorList",
    "QueryTimeSeriesRequest",
    "QueryTimeSeriesResponse",
    "MutationRecord",
    "NotificationChannel",
    "NotificationChannelDescriptor",
    "CreateNotificationChannelRequest",
    "DeleteNotificationChannelRequest",
    "GetNotificationChannelDescriptorRequest",
    "GetNotificationChannelRequest",
    "GetNotificationChannelVerificationCodeRequest",
    "GetNotificationChannelVerificationCodeResponse",
    "ListNotificationChannelDescriptorsRequest",
    "ListNotificationChannelDescriptorsResponse",
    "ListNotificationChannelsRequest",
    "ListNotificationChannelsResponse",
    "SendNotificationChannelVerificationCodeRequest",
    "UpdateNotificationChannelRequest",
    "VerifyNotificationChannelRequest",
    "BasicSli",
    "DistributionCut",
    "Range",
    "RequestBasedSli",
    "Service",
    "ServiceLevelIndicator",
    "ServiceLevelObjective",
    "TimeSeriesRatio",
    "WindowsBasedSli",
    "CreateServiceLevelObjectiveRequest",
    "CreateServiceRequest",
    "DeleteServiceLevelObjectiveRequest",
    "DeleteServiceRequest",
    "GetServiceLevelObjectiveRequest",
    "GetServiceRequest",
    "ListServiceLevelObjectivesRequest",
    "ListServiceLevelObjectivesResponse",
    "ListServicesRequest",
    "ListServicesResponse",
    "UpdateServiceLevelObjectiveRequest",
    "UpdateServiceRequest",
    "Snooze",
    "CreateSnoozeRequest",
    "GetSnoozeRequest",
    "ListSnoozesRequest",
    "ListSnoozesResponse",
    "UpdateSnoozeRequest",
    "SpanContext",
    "InternalChecker",
    "UptimeCheckConfig",
    "UptimeCheckIp",
    "GroupResourceType",
    "UptimeCheckRegion",
    "CreateUptimeCheckConfigRequest",
    "DeleteUptimeCheckConfigRequest",
    "GetUptimeCheckConfigRequest",
    "ListUptimeCheckConfigsRequest",
    "ListUptimeCheckConfigsResponse",
    "ListUptimeCheckIpsRequest",
    "ListUptimeCheckIpsResponse",
    "UpdateUptimeCheckConfigRequest",
)
