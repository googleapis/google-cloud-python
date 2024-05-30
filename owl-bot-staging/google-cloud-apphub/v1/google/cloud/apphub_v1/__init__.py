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


from .services.app_hub import AppHubClient
from .services.app_hub import AppHubAsyncClient

from .types.apphub_service import CreateApplicationRequest
from .types.apphub_service import CreateServiceProjectAttachmentRequest
from .types.apphub_service import CreateServiceRequest
from .types.apphub_service import CreateWorkloadRequest
from .types.apphub_service import DeleteApplicationRequest
from .types.apphub_service import DeleteServiceProjectAttachmentRequest
from .types.apphub_service import DeleteServiceRequest
from .types.apphub_service import DeleteWorkloadRequest
from .types.apphub_service import DetachServiceProjectAttachmentRequest
from .types.apphub_service import DetachServiceProjectAttachmentResponse
from .types.apphub_service import GetApplicationRequest
from .types.apphub_service import GetDiscoveredServiceRequest
from .types.apphub_service import GetDiscoveredWorkloadRequest
from .types.apphub_service import GetServiceProjectAttachmentRequest
from .types.apphub_service import GetServiceRequest
from .types.apphub_service import GetWorkloadRequest
from .types.apphub_service import ListApplicationsRequest
from .types.apphub_service import ListApplicationsResponse
from .types.apphub_service import ListDiscoveredServicesRequest
from .types.apphub_service import ListDiscoveredServicesResponse
from .types.apphub_service import ListDiscoveredWorkloadsRequest
from .types.apphub_service import ListDiscoveredWorkloadsResponse
from .types.apphub_service import ListServiceProjectAttachmentsRequest
from .types.apphub_service import ListServiceProjectAttachmentsResponse
from .types.apphub_service import ListServicesRequest
from .types.apphub_service import ListServicesResponse
from .types.apphub_service import ListWorkloadsRequest
from .types.apphub_service import ListWorkloadsResponse
from .types.apphub_service import LookupDiscoveredServiceRequest
from .types.apphub_service import LookupDiscoveredServiceResponse
from .types.apphub_service import LookupDiscoveredWorkloadRequest
from .types.apphub_service import LookupDiscoveredWorkloadResponse
from .types.apphub_service import LookupServiceProjectAttachmentRequest
from .types.apphub_service import LookupServiceProjectAttachmentResponse
from .types.apphub_service import OperationMetadata
from .types.apphub_service import UpdateApplicationRequest
from .types.apphub_service import UpdateServiceRequest
from .types.apphub_service import UpdateWorkloadRequest
from .types.application import Application
from .types.application import Scope
from .types.attributes import Attributes
from .types.attributes import ContactInfo
from .types.attributes import Criticality
from .types.attributes import Environment
from .types.service import DiscoveredService
from .types.service import Service
from .types.service import ServiceProperties
from .types.service import ServiceReference
from .types.service_project_attachment import ServiceProjectAttachment
from .types.workload import DiscoveredWorkload
from .types.workload import Workload
from .types.workload import WorkloadProperties
from .types.workload import WorkloadReference

__all__ = (
    'AppHubAsyncClient',
'AppHubClient',
'Application',
'Attributes',
'ContactInfo',
'CreateApplicationRequest',
'CreateServiceProjectAttachmentRequest',
'CreateServiceRequest',
'CreateWorkloadRequest',
'Criticality',
'DeleteApplicationRequest',
'DeleteServiceProjectAttachmentRequest',
'DeleteServiceRequest',
'DeleteWorkloadRequest',
'DetachServiceProjectAttachmentRequest',
'DetachServiceProjectAttachmentResponse',
'DiscoveredService',
'DiscoveredWorkload',
'Environment',
'GetApplicationRequest',
'GetDiscoveredServiceRequest',
'GetDiscoveredWorkloadRequest',
'GetServiceProjectAttachmentRequest',
'GetServiceRequest',
'GetWorkloadRequest',
'ListApplicationsRequest',
'ListApplicationsResponse',
'ListDiscoveredServicesRequest',
'ListDiscoveredServicesResponse',
'ListDiscoveredWorkloadsRequest',
'ListDiscoveredWorkloadsResponse',
'ListServiceProjectAttachmentsRequest',
'ListServiceProjectAttachmentsResponse',
'ListServicesRequest',
'ListServicesResponse',
'ListWorkloadsRequest',
'ListWorkloadsResponse',
'LookupDiscoveredServiceRequest',
'LookupDiscoveredServiceResponse',
'LookupDiscoveredWorkloadRequest',
'LookupDiscoveredWorkloadResponse',
'LookupServiceProjectAttachmentRequest',
'LookupServiceProjectAttachmentResponse',
'OperationMetadata',
'Scope',
'Service',
'ServiceProjectAttachment',
'ServiceProperties',
'ServiceReference',
'UpdateApplicationRequest',
'UpdateServiceRequest',
'UpdateWorkloadRequest',
'Workload',
'WorkloadProperties',
'WorkloadReference',
)
