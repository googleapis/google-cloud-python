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

from .services.revisions import RevisionsClient
from .services.revisions import RevisionsAsyncClient
from .services.services import ServicesClient
from .services.services import ServicesAsyncClient

from .types.condition import Condition
from .types.k8s_min import CloudSqlInstance
from .types.k8s_min import Container
from .types.k8s_min import ContainerPort
from .types.k8s_min import EnvVar
from .types.k8s_min import EnvVarSource
from .types.k8s_min import ResourceRequirements
from .types.k8s_min import SecretKeySelector
from .types.k8s_min import SecretVolumeSource
from .types.k8s_min import VersionToPath
from .types.k8s_min import Volume
from .types.k8s_min import VolumeMount
from .types.revision import DeleteRevisionRequest
from .types.revision import GetRevisionRequest
from .types.revision import ListRevisionsRequest
from .types.revision import ListRevisionsResponse
from .types.revision import Revision
from .types.revision_template import RevisionTemplate
from .types.service import CreateServiceRequest
from .types.service import DeleteServiceRequest
from .types.service import GetServiceRequest
from .types.service import ListServicesRequest
from .types.service import ListServicesResponse
from .types.service import Service
from .types.service import UpdateServiceRequest
from .types.traffic_target import TrafficTarget
from .types.traffic_target import TrafficTargetStatus
from .types.traffic_target import TrafficTargetAllocationType
from .types.vendor_settings import BinaryAuthorization
from .types.vendor_settings import RevisionScaling
from .types.vendor_settings import VpcAccess
from .types.vendor_settings import ExecutionEnvironment
from .types.vendor_settings import IngressTraffic

__all__ = (
    "RevisionsAsyncClient",
    "ServicesAsyncClient",
    "BinaryAuthorization",
    "CloudSqlInstance",
    "Condition",
    "Container",
    "ContainerPort",
    "CreateServiceRequest",
    "DeleteRevisionRequest",
    "DeleteServiceRequest",
    "EnvVar",
    "EnvVarSource",
    "ExecutionEnvironment",
    "GetRevisionRequest",
    "GetServiceRequest",
    "IngressTraffic",
    "ListRevisionsRequest",
    "ListRevisionsResponse",
    "ListServicesRequest",
    "ListServicesResponse",
    "ResourceRequirements",
    "Revision",
    "RevisionScaling",
    "RevisionTemplate",
    "RevisionsClient",
    "SecretKeySelector",
    "SecretVolumeSource",
    "Service",
    "ServicesClient",
    "TrafficTarget",
    "TrafficTargetAllocationType",
    "TrafficTargetStatus",
    "UpdateServiceRequest",
    "VersionToPath",
    "Volume",
    "VolumeMount",
    "VpcAccess",
)
