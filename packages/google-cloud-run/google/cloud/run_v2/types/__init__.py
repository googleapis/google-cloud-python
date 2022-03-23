# -*- coding: utf-8 -*-
# Copyright 2022 Google LLC
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
from .condition import Condition
from .k8s_min import (
    CloudSqlInstance,
    Container,
    ContainerPort,
    EnvVar,
    EnvVarSource,
    ResourceRequirements,
    SecretKeySelector,
    SecretVolumeSource,
    VersionToPath,
    Volume,
    VolumeMount,
)
from .revision import (
    DeleteRevisionRequest,
    GetRevisionRequest,
    ListRevisionsRequest,
    ListRevisionsResponse,
    Revision,
)
from .revision_template import RevisionTemplate
from .service import (
    CreateServiceRequest,
    DeleteServiceRequest,
    GetServiceRequest,
    ListServicesRequest,
    ListServicesResponse,
    Service,
    UpdateServiceRequest,
)
from .traffic_target import (
    TrafficTarget,
    TrafficTargetStatus,
    TrafficTargetAllocationType,
)
from .vendor_settings import (
    BinaryAuthorization,
    RevisionScaling,
    VpcAccess,
    ExecutionEnvironment,
    IngressTraffic,
)

__all__ = (
    "Condition",
    "CloudSqlInstance",
    "Container",
    "ContainerPort",
    "EnvVar",
    "EnvVarSource",
    "ResourceRequirements",
    "SecretKeySelector",
    "SecretVolumeSource",
    "VersionToPath",
    "Volume",
    "VolumeMount",
    "DeleteRevisionRequest",
    "GetRevisionRequest",
    "ListRevisionsRequest",
    "ListRevisionsResponse",
    "Revision",
    "RevisionTemplate",
    "CreateServiceRequest",
    "DeleteServiceRequest",
    "GetServiceRequest",
    "ListServicesRequest",
    "ListServicesResponse",
    "Service",
    "UpdateServiceRequest",
    "TrafficTarget",
    "TrafficTargetStatus",
    "TrafficTargetAllocationType",
    "BinaryAuthorization",
    "RevisionScaling",
    "VpcAccess",
    "ExecutionEnvironment",
    "IngressTraffic",
)
