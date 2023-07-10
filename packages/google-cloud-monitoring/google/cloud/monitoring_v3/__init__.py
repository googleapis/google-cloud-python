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
from google.cloud.monitoring_v3 import gapic_version as package_version

__version__ = package_version.__version__


from .services.alert_policy_service import AlertPolicyServiceClient
from .services.alert_policy_service import AlertPolicyServiceAsyncClient
from .services.group_service import GroupServiceClient
from .services.group_service import GroupServiceAsyncClient
from .services.metric_service import MetricServiceClient
from .services.metric_service import MetricServiceAsyncClient
from .services.notification_channel_service import NotificationChannelServiceClient
from .services.notification_channel_service import NotificationChannelServiceAsyncClient
from .services.query_service import QueryServiceClient
from .services.query_service import QueryServiceAsyncClient
from .services.service_monitoring_service import ServiceMonitoringServiceClient
from .services.service_monitoring_service import ServiceMonitoringServiceAsyncClient
from .services.snooze_service import SnoozeServiceClient
from .services.snooze_service import SnoozeServiceAsyncClient
from .services.uptime_check_service import UptimeCheckServiceClient
from .services.uptime_check_service import UptimeCheckServiceAsyncClient

from .types.alert import AlertPolicy
from .types.alert_service import CreateAlertPolicyRequest
from .types.alert_service import DeleteAlertPolicyRequest
from .types.alert_service import GetAlertPolicyRequest
from .types.alert_service import ListAlertPoliciesRequest
from .types.alert_service import ListAlertPoliciesResponse
from .types.alert_service import UpdateAlertPolicyRequest
from .types.common import Aggregation
from .types.common import TimeInterval
from .types.common import TypedValue
from .types.common import ComparisonType
from .types.common import ServiceTier
from .types.dropped_labels import DroppedLabels
from .types.group import Group
from .types.group_service import CreateGroupRequest
from .types.group_service import DeleteGroupRequest
from .types.group_service import GetGroupRequest
from .types.group_service import ListGroupMembersRequest
from .types.group_service import ListGroupMembersResponse
from .types.group_service import ListGroupsRequest
from .types.group_service import ListGroupsResponse
from .types.group_service import UpdateGroupRequest
from .types.metric import LabelValue
from .types.metric import Point
from .types.metric import QueryError
from .types.metric import TextLocator
from .types.metric import TimeSeries
from .types.metric import TimeSeriesData
from .types.metric import TimeSeriesDescriptor
from .types.metric_service import CreateMetricDescriptorRequest
from .types.metric_service import CreateTimeSeriesError
from .types.metric_service import CreateTimeSeriesRequest
from .types.metric_service import CreateTimeSeriesSummary
from .types.metric_service import DeleteMetricDescriptorRequest
from .types.metric_service import GetMetricDescriptorRequest
from .types.metric_service import GetMonitoredResourceDescriptorRequest
from .types.metric_service import ListMetricDescriptorsRequest
from .types.metric_service import ListMetricDescriptorsResponse
from .types.metric_service import ListMonitoredResourceDescriptorsRequest
from .types.metric_service import ListMonitoredResourceDescriptorsResponse
from .types.metric_service import ListTimeSeriesRequest
from .types.metric_service import ListTimeSeriesResponse
from .types.metric_service import QueryErrorList
from .types.metric_service import QueryTimeSeriesRequest
from .types.metric_service import QueryTimeSeriesResponse
from .types.mutation_record import MutationRecord
from .types.notification import NotificationChannel
from .types.notification import NotificationChannelDescriptor
from .types.notification_service import CreateNotificationChannelRequest
from .types.notification_service import DeleteNotificationChannelRequest
from .types.notification_service import GetNotificationChannelDescriptorRequest
from .types.notification_service import GetNotificationChannelRequest
from .types.notification_service import GetNotificationChannelVerificationCodeRequest
from .types.notification_service import GetNotificationChannelVerificationCodeResponse
from .types.notification_service import ListNotificationChannelDescriptorsRequest
from .types.notification_service import ListNotificationChannelDescriptorsResponse
from .types.notification_service import ListNotificationChannelsRequest
from .types.notification_service import ListNotificationChannelsResponse
from .types.notification_service import SendNotificationChannelVerificationCodeRequest
from .types.notification_service import UpdateNotificationChannelRequest
from .types.notification_service import VerifyNotificationChannelRequest
from .types.service import BasicSli
from .types.service import DistributionCut
from .types.service import Range
from .types.service import RequestBasedSli
from .types.service import Service
from .types.service import ServiceLevelIndicator
from .types.service import ServiceLevelObjective
from .types.service import TimeSeriesRatio
from .types.service import WindowsBasedSli
from .types.service_service import CreateServiceLevelObjectiveRequest
from .types.service_service import CreateServiceRequest
from .types.service_service import DeleteServiceLevelObjectiveRequest
from .types.service_service import DeleteServiceRequest
from .types.service_service import GetServiceLevelObjectiveRequest
from .types.service_service import GetServiceRequest
from .types.service_service import ListServiceLevelObjectivesRequest
from .types.service_service import ListServiceLevelObjectivesResponse
from .types.service_service import ListServicesRequest
from .types.service_service import ListServicesResponse
from .types.service_service import UpdateServiceLevelObjectiveRequest
from .types.service_service import UpdateServiceRequest
from .types.snooze import Snooze
from .types.snooze_service import CreateSnoozeRequest
from .types.snooze_service import GetSnoozeRequest
from .types.snooze_service import ListSnoozesRequest
from .types.snooze_service import ListSnoozesResponse
from .types.snooze_service import UpdateSnoozeRequest
from .types.span_context import SpanContext
from .types.uptime import InternalChecker
from .types.uptime import UptimeCheckConfig
from .types.uptime import UptimeCheckIp
from .types.uptime import GroupResourceType
from .types.uptime import UptimeCheckRegion
from .types.uptime_service import CreateUptimeCheckConfigRequest
from .types.uptime_service import DeleteUptimeCheckConfigRequest
from .types.uptime_service import GetUptimeCheckConfigRequest
from .types.uptime_service import ListUptimeCheckConfigsRequest
from .types.uptime_service import ListUptimeCheckConfigsResponse
from .types.uptime_service import ListUptimeCheckIpsRequest
from .types.uptime_service import ListUptimeCheckIpsResponse
from .types.uptime_service import UpdateUptimeCheckConfigRequest

__all__ = (
    "AlertPolicyServiceAsyncClient",
    "GroupServiceAsyncClient",
    "MetricServiceAsyncClient",
    "NotificationChannelServiceAsyncClient",
    "QueryServiceAsyncClient",
    "ServiceMonitoringServiceAsyncClient",
    "SnoozeServiceAsyncClient",
    "UptimeCheckServiceAsyncClient",
    "Aggregation",
    "AlertPolicy",
    "AlertPolicyServiceClient",
    "BasicSli",
    "ComparisonType",
    "CreateAlertPolicyRequest",
    "CreateGroupRequest",
    "CreateMetricDescriptorRequest",
    "CreateNotificationChannelRequest",
    "CreateServiceLevelObjectiveRequest",
    "CreateServiceRequest",
    "CreateSnoozeRequest",
    "CreateTimeSeriesError",
    "CreateTimeSeriesRequest",
    "CreateTimeSeriesSummary",
    "CreateUptimeCheckConfigRequest",
    "DeleteAlertPolicyRequest",
    "DeleteGroupRequest",
    "DeleteMetricDescriptorRequest",
    "DeleteNotificationChannelRequest",
    "DeleteServiceLevelObjectiveRequest",
    "DeleteServiceRequest",
    "DeleteUptimeCheckConfigRequest",
    "DistributionCut",
    "DroppedLabels",
    "GetAlertPolicyRequest",
    "GetGroupRequest",
    "GetMetricDescriptorRequest",
    "GetMonitoredResourceDescriptorRequest",
    "GetNotificationChannelDescriptorRequest",
    "GetNotificationChannelRequest",
    "GetNotificationChannelVerificationCodeRequest",
    "GetNotificationChannelVerificationCodeResponse",
    "GetServiceLevelObjectiveRequest",
    "GetServiceRequest",
    "GetSnoozeRequest",
    "GetUptimeCheckConfigRequest",
    "Group",
    "GroupResourceType",
    "GroupServiceClient",
    "InternalChecker",
    "LabelValue",
    "ListAlertPoliciesRequest",
    "ListAlertPoliciesResponse",
    "ListGroupMembersRequest",
    "ListGroupMembersResponse",
    "ListGroupsRequest",
    "ListGroupsResponse",
    "ListMetricDescriptorsRequest",
    "ListMetricDescriptorsResponse",
    "ListMonitoredResourceDescriptorsRequest",
    "ListMonitoredResourceDescriptorsResponse",
    "ListNotificationChannelDescriptorsRequest",
    "ListNotificationChannelDescriptorsResponse",
    "ListNotificationChannelsRequest",
    "ListNotificationChannelsResponse",
    "ListServiceLevelObjectivesRequest",
    "ListServiceLevelObjectivesResponse",
    "ListServicesRequest",
    "ListServicesResponse",
    "ListSnoozesRequest",
    "ListSnoozesResponse",
    "ListTimeSeriesRequest",
    "ListTimeSeriesResponse",
    "ListUptimeCheckConfigsRequest",
    "ListUptimeCheckConfigsResponse",
    "ListUptimeCheckIpsRequest",
    "ListUptimeCheckIpsResponse",
    "MetricServiceClient",
    "MutationRecord",
    "NotificationChannel",
    "NotificationChannelDescriptor",
    "NotificationChannelServiceClient",
    "Point",
    "QueryError",
    "QueryErrorList",
    "QueryServiceClient",
    "QueryTimeSeriesRequest",
    "QueryTimeSeriesResponse",
    "Range",
    "RequestBasedSli",
    "SendNotificationChannelVerificationCodeRequest",
    "Service",
    "ServiceLevelIndicator",
    "ServiceLevelObjective",
    "ServiceMonitoringServiceClient",
    "ServiceTier",
    "Snooze",
    "SnoozeServiceClient",
    "SpanContext",
    "TextLocator",
    "TimeInterval",
    "TimeSeries",
    "TimeSeriesData",
    "TimeSeriesDescriptor",
    "TimeSeriesRatio",
    "TypedValue",
    "UpdateAlertPolicyRequest",
    "UpdateGroupRequest",
    "UpdateNotificationChannelRequest",
    "UpdateServiceLevelObjectiveRequest",
    "UpdateServiceRequest",
    "UpdateSnoozeRequest",
    "UpdateUptimeCheckConfigRequest",
    "UptimeCheckConfig",
    "UptimeCheckIp",
    "UptimeCheckRegion",
    "UptimeCheckServiceClient",
    "VerifyNotificationChannelRequest",
    "WindowsBasedSli",
)
