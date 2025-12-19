# -*- coding: utf-8 -*-
# Copyright 2025 Google LLC
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
import sys

import google.api_core as api_core

from google.cloud.monitoring_v3 import gapic_version as package_version

__version__ = package_version.__version__

if sys.version_info >= (3, 8):  # pragma: NO COVER
    from importlib import metadata
else:  # pragma: NO COVER
    # TODO(https://github.com/googleapis/python-api-core/issues/835): Remove
    # this code path once we drop support for Python 3.7
    import importlib_metadata as metadata

from .services.alert_policy_service import (
    AlertPolicyServiceAsyncClient,
    AlertPolicyServiceClient,
)
from .services.group_service import GroupServiceAsyncClient, GroupServiceClient
from .services.metric_service import MetricServiceAsyncClient, MetricServiceClient
from .services.notification_channel_service import (
    NotificationChannelServiceAsyncClient,
    NotificationChannelServiceClient,
)
from .services.query_service import QueryServiceAsyncClient, QueryServiceClient
from .services.service_monitoring_service import (
    ServiceMonitoringServiceAsyncClient,
    ServiceMonitoringServiceClient,
)
from .services.snooze_service import SnoozeServiceAsyncClient, SnoozeServiceClient
from .services.uptime_check_service import (
    UptimeCheckServiceAsyncClient,
    UptimeCheckServiceClient,
)
from .types.alert import AlertPolicy
from .types.alert_service import (
    CreateAlertPolicyRequest,
    DeleteAlertPolicyRequest,
    GetAlertPolicyRequest,
    ListAlertPoliciesRequest,
    ListAlertPoliciesResponse,
    UpdateAlertPolicyRequest,
)
from .types.common import (
    Aggregation,
    ComparisonType,
    ServiceTier,
    TimeInterval,
    TypedValue,
)
from .types.dropped_labels import DroppedLabels
from .types.group import Group
from .types.group_service import (
    CreateGroupRequest,
    DeleteGroupRequest,
    GetGroupRequest,
    ListGroupMembersRequest,
    ListGroupMembersResponse,
    ListGroupsRequest,
    ListGroupsResponse,
    UpdateGroupRequest,
)
from .types.metric import (
    LabelValue,
    Point,
    QueryError,
    TextLocator,
    TimeSeries,
    TimeSeriesData,
    TimeSeriesDescriptor,
)
from .types.metric_service import (
    CreateMetricDescriptorRequest,
    CreateTimeSeriesError,
    CreateTimeSeriesRequest,
    CreateTimeSeriesSummary,
    DeleteMetricDescriptorRequest,
    GetMetricDescriptorRequest,
    GetMonitoredResourceDescriptorRequest,
    ListMetricDescriptorsRequest,
    ListMetricDescriptorsResponse,
    ListMonitoredResourceDescriptorsRequest,
    ListMonitoredResourceDescriptorsResponse,
    ListTimeSeriesRequest,
    ListTimeSeriesResponse,
    QueryErrorList,
    QueryTimeSeriesRequest,
    QueryTimeSeriesResponse,
)
from .types.mutation_record import MutationRecord
from .types.notification import NotificationChannel, NotificationChannelDescriptor
from .types.notification_service import (
    CreateNotificationChannelRequest,
    DeleteNotificationChannelRequest,
    GetNotificationChannelDescriptorRequest,
    GetNotificationChannelRequest,
    GetNotificationChannelVerificationCodeRequest,
    GetNotificationChannelVerificationCodeResponse,
    ListNotificationChannelDescriptorsRequest,
    ListNotificationChannelDescriptorsResponse,
    ListNotificationChannelsRequest,
    ListNotificationChannelsResponse,
    SendNotificationChannelVerificationCodeRequest,
    UpdateNotificationChannelRequest,
    VerifyNotificationChannelRequest,
)
from .types.service import (
    BasicSli,
    DistributionCut,
    Range,
    RequestBasedSli,
    Service,
    ServiceLevelIndicator,
    ServiceLevelObjective,
    TimeSeriesRatio,
    WindowsBasedSli,
)
from .types.service_service import (
    CreateServiceLevelObjectiveRequest,
    CreateServiceRequest,
    DeleteServiceLevelObjectiveRequest,
    DeleteServiceRequest,
    GetServiceLevelObjectiveRequest,
    GetServiceRequest,
    ListServiceLevelObjectivesRequest,
    ListServiceLevelObjectivesResponse,
    ListServicesRequest,
    ListServicesResponse,
    UpdateServiceLevelObjectiveRequest,
    UpdateServiceRequest,
)
from .types.snooze import Snooze
from .types.snooze_service import (
    CreateSnoozeRequest,
    GetSnoozeRequest,
    ListSnoozesRequest,
    ListSnoozesResponse,
    UpdateSnoozeRequest,
)
from .types.span_context import SpanContext
from .types.uptime import (
    GroupResourceType,
    InternalChecker,
    SyntheticMonitorTarget,
    UptimeCheckConfig,
    UptimeCheckIp,
    UptimeCheckRegion,
)
from .types.uptime_service import (
    CreateUptimeCheckConfigRequest,
    DeleteUptimeCheckConfigRequest,
    GetUptimeCheckConfigRequest,
    ListUptimeCheckConfigsRequest,
    ListUptimeCheckConfigsResponse,
    ListUptimeCheckIpsRequest,
    ListUptimeCheckIpsResponse,
    UpdateUptimeCheckConfigRequest,
)

if hasattr(api_core, "check_python_version") and hasattr(
    api_core, "check_dependency_versions"
):  # pragma: NO COVER
    api_core.check_python_version("google.cloud.monitoring_v3")  # type: ignore
    api_core.check_dependency_versions("google.cloud.monitoring_v3")  # type: ignore
else:  # pragma: NO COVER
    # An older version of api_core is installed which does not define the
    # functions above. We do equivalent checks manually.
    try:
        import sys
        import warnings

        _py_version_str = sys.version.split()[0]
        _package_label = "google.cloud.monitoring_v3"
        if sys.version_info < (3, 9):
            warnings.warn(
                "You are using a non-supported Python version "
                + f"({_py_version_str}).  Google will not post any further "
                + f"updates to {_package_label} supporting this Python version. "
                + "Please upgrade to the latest Python version, or at "
                + f"least to Python 3.9, and then update {_package_label}.",
                FutureWarning,
            )
        if sys.version_info[:2] == (3, 9):
            warnings.warn(
                f"You are using a Python version ({_py_version_str}) "
                + f"which Google will stop supporting in {_package_label} in "
                + "January 2026. Please "
                + "upgrade to the latest Python version, or at "
                + "least to Python 3.10, before then, and "
                + f"then update {_package_label}.",
                FutureWarning,
            )

        def parse_version_to_tuple(version_string: str):
            """Safely converts a semantic version string to a comparable tuple of integers.
            Example: "4.25.8" -> (4, 25, 8)
            Ignores non-numeric parts and handles common version formats.
            Args:
                version_string: Version string in the format "x.y.z" or "x.y.z<suffix>"
            Returns:
                Tuple of integers for the parsed version string.
            """
            parts = []
            for part in version_string.split("."):
                try:
                    parts.append(int(part))
                except ValueError:
                    # If it's a non-numeric part (e.g., '1.0.0b1' -> 'b1'), stop here.
                    # This is a simplification compared to 'packaging.parse_version', but sufficient
                    # for comparing strictly numeric semantic versions.
                    break
            return tuple(parts)

        def _get_version(dependency_name):
            try:
                version_string: str = metadata.version(dependency_name)
                parsed_version = parse_version_to_tuple(version_string)
                return (parsed_version, version_string)
            except Exception:
                # Catch exceptions from metadata.version() (e.g., PackageNotFoundError)
                # or errors during parse_version_to_tuple
                return (None, "--")

        _dependency_package = "google.protobuf"
        _next_supported_version = "4.25.8"
        _next_supported_version_tuple = (4, 25, 8)
        _recommendation = " (we recommend 6.x)"
        (_version_used, _version_used_string) = _get_version(_dependency_package)
        if _version_used and _version_used < _next_supported_version_tuple:
            warnings.warn(
                f"Package {_package_label} depends on "
                + f"{_dependency_package}, currently installed at version "
                + f"{_version_used_string}. Future updates to "
                + f"{_package_label} will require {_dependency_package} at "
                + f"version {_next_supported_version} or higher{_recommendation}."
                + " Please ensure "
                + "that either (a) your Python environment doesn't pin the "
                + f"version of {_dependency_package}, so that updates to "
                + f"{_package_label} can require the higher version, or "
                + "(b) you manually update your Python environment to use at "
                + f"least version {_next_supported_version} of "
                + f"{_dependency_package}.",
                FutureWarning,
            )
    except Exception:
        warnings.warn(
            "Could not determine the version of Python "
            + "currently being used. To continue receiving "
            + "updates for {_package_label}, ensure you are "
            + "using a supported version of Python; see "
            + "https://devguide.python.org/versions/"
        )

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
    "SyntheticMonitorTarget",
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
