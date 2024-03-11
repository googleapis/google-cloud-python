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
from google.cloud.apphub_v1 import gapic_version as package_version

__version__ = package_version.__version__


from .services.app_hub import AppHubAsyncClient, AppHubClient
from .types.apphub_service import (
    CreateApplicationRequest,
    CreateServiceProjectAttachmentRequest,
    CreateServiceRequest,
    CreateWorkloadRequest,
    DeleteApplicationRequest,
    DeleteServiceProjectAttachmentRequest,
    DeleteServiceRequest,
    DeleteWorkloadRequest,
    DetachServiceProjectAttachmentRequest,
    DetachServiceProjectAttachmentResponse,
    GetApplicationRequest,
    GetDiscoveredServiceRequest,
    GetDiscoveredWorkloadRequest,
    GetServiceProjectAttachmentRequest,
    GetServiceRequest,
    GetWorkloadRequest,
    ListApplicationsRequest,
    ListApplicationsResponse,
    ListDiscoveredServicesRequest,
    ListDiscoveredServicesResponse,
    ListDiscoveredWorkloadsRequest,
    ListDiscoveredWorkloadsResponse,
    ListServiceProjectAttachmentsRequest,
    ListServiceProjectAttachmentsResponse,
    ListServicesRequest,
    ListServicesResponse,
    ListWorkloadsRequest,
    ListWorkloadsResponse,
    LookupDiscoveredServiceRequest,
    LookupDiscoveredServiceResponse,
    LookupDiscoveredWorkloadRequest,
    LookupDiscoveredWorkloadResponse,
    LookupServiceProjectAttachmentRequest,
    LookupServiceProjectAttachmentResponse,
    OperationMetadata,
    UpdateApplicationRequest,
    UpdateServiceRequest,
    UpdateWorkloadRequest,
)
from .types.application import Application, Scope
from .types.attributes import Attributes, ContactInfo, Criticality, Environment
from .types.service import (
    DiscoveredService,
    Service,
    ServiceProperties,
    ServiceReference,
)
from .types.service_project_attachment import ServiceProjectAttachment
from .types.workload import (
    DiscoveredWorkload,
    Workload,
    WorkloadProperties,
    WorkloadReference,
)

__all__ = (
    "AppHubAsyncClient",
    "AppHubClient",
    "Application",
    "Attributes",
    "ContactInfo",
    "CreateApplicationRequest",
    "CreateServiceProjectAttachmentRequest",
    "CreateServiceRequest",
    "CreateWorkloadRequest",
    "Criticality",
    "DeleteApplicationRequest",
    "DeleteServiceProjectAttachmentRequest",
    "DeleteServiceRequest",
    "DeleteWorkloadRequest",
    "DetachServiceProjectAttachmentRequest",
    "DetachServiceProjectAttachmentResponse",
    "DiscoveredService",
    "DiscoveredWorkload",
    "Environment",
    "GetApplicationRequest",
    "GetDiscoveredServiceRequest",
    "GetDiscoveredWorkloadRequest",
    "GetServiceProjectAttachmentRequest",
    "GetServiceRequest",
    "GetWorkloadRequest",
    "ListApplicationsRequest",
    "ListApplicationsResponse",
    "ListDiscoveredServicesRequest",
    "ListDiscoveredServicesResponse",
    "ListDiscoveredWorkloadsRequest",
    "ListDiscoveredWorkloadsResponse",
    "ListServiceProjectAttachmentsRequest",
    "ListServiceProjectAttachmentsResponse",
    "ListServicesRequest",
    "ListServicesResponse",
    "ListWorkloadsRequest",
    "ListWorkloadsResponse",
    "LookupDiscoveredServiceRequest",
    "LookupDiscoveredServiceResponse",
    "LookupDiscoveredWorkloadRequest",
    "LookupDiscoveredWorkloadResponse",
    "LookupServiceProjectAttachmentRequest",
    "LookupServiceProjectAttachmentResponse",
    "OperationMetadata",
    "Scope",
    "Service",
    "ServiceProjectAttachment",
    "ServiceProperties",
    "ServiceReference",
    "UpdateApplicationRequest",
    "UpdateServiceRequest",
    "UpdateWorkloadRequest",
    "Workload",
    "WorkloadProperties",
    "WorkloadReference",
)
