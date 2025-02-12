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
from google.cloud.apphub import gapic_version as package_version

__version__ = package_version.__version__


from google.cloud.apphub_v1.services.app_hub.client import AppHubClient
from google.cloud.apphub_v1.services.app_hub.async_client import AppHubAsyncClient

from google.cloud.apphub_v1.types.apphub_service import CreateApplicationRequest
from google.cloud.apphub_v1.types.apphub_service import CreateServiceProjectAttachmentRequest
from google.cloud.apphub_v1.types.apphub_service import CreateServiceRequest
from google.cloud.apphub_v1.types.apphub_service import CreateWorkloadRequest
from google.cloud.apphub_v1.types.apphub_service import DeleteApplicationRequest
from google.cloud.apphub_v1.types.apphub_service import DeleteServiceProjectAttachmentRequest
from google.cloud.apphub_v1.types.apphub_service import DeleteServiceRequest
from google.cloud.apphub_v1.types.apphub_service import DeleteWorkloadRequest
from google.cloud.apphub_v1.types.apphub_service import DetachServiceProjectAttachmentRequest
from google.cloud.apphub_v1.types.apphub_service import DetachServiceProjectAttachmentResponse
from google.cloud.apphub_v1.types.apphub_service import GetApplicationRequest
from google.cloud.apphub_v1.types.apphub_service import GetDiscoveredServiceRequest
from google.cloud.apphub_v1.types.apphub_service import GetDiscoveredWorkloadRequest
from google.cloud.apphub_v1.types.apphub_service import GetServiceProjectAttachmentRequest
from google.cloud.apphub_v1.types.apphub_service import GetServiceRequest
from google.cloud.apphub_v1.types.apphub_service import GetWorkloadRequest
from google.cloud.apphub_v1.types.apphub_service import ListApplicationsRequest
from google.cloud.apphub_v1.types.apphub_service import ListApplicationsResponse
from google.cloud.apphub_v1.types.apphub_service import ListDiscoveredServicesRequest
from google.cloud.apphub_v1.types.apphub_service import ListDiscoveredServicesResponse
from google.cloud.apphub_v1.types.apphub_service import ListDiscoveredWorkloadsRequest
from google.cloud.apphub_v1.types.apphub_service import ListDiscoveredWorkloadsResponse
from google.cloud.apphub_v1.types.apphub_service import ListServiceProjectAttachmentsRequest
from google.cloud.apphub_v1.types.apphub_service import ListServiceProjectAttachmentsResponse
from google.cloud.apphub_v1.types.apphub_service import ListServicesRequest
from google.cloud.apphub_v1.types.apphub_service import ListServicesResponse
from google.cloud.apphub_v1.types.apphub_service import ListWorkloadsRequest
from google.cloud.apphub_v1.types.apphub_service import ListWorkloadsResponse
from google.cloud.apphub_v1.types.apphub_service import LookupDiscoveredServiceRequest
from google.cloud.apphub_v1.types.apphub_service import LookupDiscoveredServiceResponse
from google.cloud.apphub_v1.types.apphub_service import LookupDiscoveredWorkloadRequest
from google.cloud.apphub_v1.types.apphub_service import LookupDiscoveredWorkloadResponse
from google.cloud.apphub_v1.types.apphub_service import LookupServiceProjectAttachmentRequest
from google.cloud.apphub_v1.types.apphub_service import LookupServiceProjectAttachmentResponse
from google.cloud.apphub_v1.types.apphub_service import OperationMetadata
from google.cloud.apphub_v1.types.apphub_service import UpdateApplicationRequest
from google.cloud.apphub_v1.types.apphub_service import UpdateServiceRequest
from google.cloud.apphub_v1.types.apphub_service import UpdateWorkloadRequest
from google.cloud.apphub_v1.types.application import Application
from google.cloud.apphub_v1.types.application import Scope
from google.cloud.apphub_v1.types.attributes import Attributes
from google.cloud.apphub_v1.types.attributes import ContactInfo
from google.cloud.apphub_v1.types.attributes import Criticality
from google.cloud.apphub_v1.types.attributes import Environment
from google.cloud.apphub_v1.types.service import DiscoveredService
from google.cloud.apphub_v1.types.service import Service
from google.cloud.apphub_v1.types.service import ServiceProperties
from google.cloud.apphub_v1.types.service import ServiceReference
from google.cloud.apphub_v1.types.service_project_attachment import ServiceProjectAttachment
from google.cloud.apphub_v1.types.workload import DiscoveredWorkload
from google.cloud.apphub_v1.types.workload import Workload
from google.cloud.apphub_v1.types.workload import WorkloadProperties
from google.cloud.apphub_v1.types.workload import WorkloadReference

__all__ = ('AppHubClient',
    'AppHubAsyncClient',
    'CreateApplicationRequest',
    'CreateServiceProjectAttachmentRequest',
    'CreateServiceRequest',
    'CreateWorkloadRequest',
    'DeleteApplicationRequest',
    'DeleteServiceProjectAttachmentRequest',
    'DeleteServiceRequest',
    'DeleteWorkloadRequest',
    'DetachServiceProjectAttachmentRequest',
    'DetachServiceProjectAttachmentResponse',
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
    'UpdateApplicationRequest',
    'UpdateServiceRequest',
    'UpdateWorkloadRequest',
    'Application',
    'Scope',
    'Attributes',
    'ContactInfo',
    'Criticality',
    'Environment',
    'DiscoveredService',
    'Service',
    'ServiceProperties',
    'ServiceReference',
    'ServiceProjectAttachment',
    'DiscoveredWorkload',
    'Workload',
    'WorkloadProperties',
    'WorkloadReference',
)
