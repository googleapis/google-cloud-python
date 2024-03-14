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
from .apphub_service import (
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
from .application import Application, Scope
from .attributes import Attributes, ContactInfo, Criticality, Environment
from .service import DiscoveredService, Service, ServiceProperties, ServiceReference
from .service_project_attachment import ServiceProjectAttachment
from .workload import (
    DiscoveredWorkload,
    Workload,
    WorkloadProperties,
    WorkloadReference,
)

__all__ = (
    "CreateApplicationRequest",
    "CreateServiceProjectAttachmentRequest",
    "CreateServiceRequest",
    "CreateWorkloadRequest",
    "DeleteApplicationRequest",
    "DeleteServiceProjectAttachmentRequest",
    "DeleteServiceRequest",
    "DeleteWorkloadRequest",
    "DetachServiceProjectAttachmentRequest",
    "DetachServiceProjectAttachmentResponse",
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
    "UpdateApplicationRequest",
    "UpdateServiceRequest",
    "UpdateWorkloadRequest",
    "Application",
    "Scope",
    "Attributes",
    "ContactInfo",
    "Criticality",
    "Environment",
    "DiscoveredService",
    "Service",
    "ServiceProperties",
    "ServiceReference",
    "ServiceProjectAttachment",
    "DiscoveredWorkload",
    "Workload",
    "WorkloadProperties",
    "WorkloadReference",
)
