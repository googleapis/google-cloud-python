# -*- coding: utf-8 -*-
# Copyright 2020 Google LLC
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

from google.cloud.talent_v4.services.company_service.client import CompanyServiceClient
from google.cloud.talent_v4.services.company_service.async_client import (
    CompanyServiceAsyncClient,
)
from google.cloud.talent_v4.services.completion.client import CompletionClient
from google.cloud.talent_v4.services.completion.async_client import (
    CompletionAsyncClient,
)
from google.cloud.talent_v4.services.event_service.client import EventServiceClient
from google.cloud.talent_v4.services.event_service.async_client import (
    EventServiceAsyncClient,
)
from google.cloud.talent_v4.services.job_service.client import JobServiceClient
from google.cloud.talent_v4.services.job_service.async_client import (
    JobServiceAsyncClient,
)
from google.cloud.talent_v4.services.tenant_service.client import TenantServiceClient
from google.cloud.talent_v4.services.tenant_service.async_client import (
    TenantServiceAsyncClient,
)

from google.cloud.talent_v4.types.common import BatchOperationMetadata
from google.cloud.talent_v4.types.common import CompensationInfo
from google.cloud.talent_v4.types.common import CustomAttribute
from google.cloud.talent_v4.types.common import DeviceInfo
from google.cloud.talent_v4.types.common import Location
from google.cloud.talent_v4.types.common import RequestMetadata
from google.cloud.talent_v4.types.common import ResponseMetadata
from google.cloud.talent_v4.types.common import SpellingCorrection
from google.cloud.talent_v4.types.common import TimestampRange
from google.cloud.talent_v4.types.common import CommuteMethod
from google.cloud.talent_v4.types.common import CompanySize
from google.cloud.talent_v4.types.common import DegreeType
from google.cloud.talent_v4.types.common import EmploymentType
from google.cloud.talent_v4.types.common import HtmlSanitization
from google.cloud.talent_v4.types.common import JobBenefit
from google.cloud.talent_v4.types.common import JobCategory
from google.cloud.talent_v4.types.common import JobLevel
from google.cloud.talent_v4.types.common import PostingRegion
from google.cloud.talent_v4.types.common import Visibility
from google.cloud.talent_v4.types.company import Company
from google.cloud.talent_v4.types.company_service import CreateCompanyRequest
from google.cloud.talent_v4.types.company_service import DeleteCompanyRequest
from google.cloud.talent_v4.types.company_service import GetCompanyRequest
from google.cloud.talent_v4.types.company_service import ListCompaniesRequest
from google.cloud.talent_v4.types.company_service import ListCompaniesResponse
from google.cloud.talent_v4.types.company_service import UpdateCompanyRequest
from google.cloud.talent_v4.types.completion_service import CompleteQueryRequest
from google.cloud.talent_v4.types.completion_service import CompleteQueryResponse
from google.cloud.talent_v4.types.event import ClientEvent
from google.cloud.talent_v4.types.event import JobEvent
from google.cloud.talent_v4.types.event_service import CreateClientEventRequest
from google.cloud.talent_v4.types.filters import CommuteFilter
from google.cloud.talent_v4.types.filters import CompensationFilter
from google.cloud.talent_v4.types.filters import JobQuery
from google.cloud.talent_v4.types.filters import LocationFilter
from google.cloud.talent_v4.types.histogram import HistogramQuery
from google.cloud.talent_v4.types.histogram import HistogramQueryResult
from google.cloud.talent_v4.types.job import Job
from google.cloud.talent_v4.types.job_service import BatchCreateJobsRequest
from google.cloud.talent_v4.types.job_service import BatchCreateJobsResponse
from google.cloud.talent_v4.types.job_service import BatchDeleteJobsRequest
from google.cloud.talent_v4.types.job_service import BatchDeleteJobsResponse
from google.cloud.talent_v4.types.job_service import BatchUpdateJobsRequest
from google.cloud.talent_v4.types.job_service import BatchUpdateJobsResponse
from google.cloud.talent_v4.types.job_service import CreateJobRequest
from google.cloud.talent_v4.types.job_service import DeleteJobRequest
from google.cloud.talent_v4.types.job_service import GetJobRequest
from google.cloud.talent_v4.types.job_service import JobResult
from google.cloud.talent_v4.types.job_service import ListJobsRequest
from google.cloud.talent_v4.types.job_service import ListJobsResponse
from google.cloud.talent_v4.types.job_service import SearchJobsRequest
from google.cloud.talent_v4.types.job_service import SearchJobsResponse
from google.cloud.talent_v4.types.job_service import UpdateJobRequest
from google.cloud.talent_v4.types.job_service import JobView
from google.cloud.talent_v4.types.tenant import Tenant
from google.cloud.talent_v4.types.tenant_service import CreateTenantRequest
from google.cloud.talent_v4.types.tenant_service import DeleteTenantRequest
from google.cloud.talent_v4.types.tenant_service import GetTenantRequest
from google.cloud.talent_v4.types.tenant_service import ListTenantsRequest
from google.cloud.talent_v4.types.tenant_service import ListTenantsResponse
from google.cloud.talent_v4.types.tenant_service import UpdateTenantRequest

__all__ = (
    "CompanyServiceClient",
    "CompanyServiceAsyncClient",
    "CompletionClient",
    "CompletionAsyncClient",
    "EventServiceClient",
    "EventServiceAsyncClient",
    "JobServiceClient",
    "JobServiceAsyncClient",
    "TenantServiceClient",
    "TenantServiceAsyncClient",
    "BatchOperationMetadata",
    "CompensationInfo",
    "CustomAttribute",
    "DeviceInfo",
    "Location",
    "RequestMetadata",
    "ResponseMetadata",
    "SpellingCorrection",
    "TimestampRange",
    "CommuteMethod",
    "CompanySize",
    "DegreeType",
    "EmploymentType",
    "HtmlSanitization",
    "JobBenefit",
    "JobCategory",
    "JobLevel",
    "PostingRegion",
    "Visibility",
    "Company",
    "CreateCompanyRequest",
    "DeleteCompanyRequest",
    "GetCompanyRequest",
    "ListCompaniesRequest",
    "ListCompaniesResponse",
    "UpdateCompanyRequest",
    "CompleteQueryRequest",
    "CompleteQueryResponse",
    "ClientEvent",
    "JobEvent",
    "CreateClientEventRequest",
    "CommuteFilter",
    "CompensationFilter",
    "JobQuery",
    "LocationFilter",
    "HistogramQuery",
    "HistogramQueryResult",
    "Job",
    "BatchCreateJobsRequest",
    "BatchCreateJobsResponse",
    "BatchDeleteJobsRequest",
    "BatchDeleteJobsResponse",
    "BatchUpdateJobsRequest",
    "BatchUpdateJobsResponse",
    "CreateJobRequest",
    "DeleteJobRequest",
    "GetJobRequest",
    "JobResult",
    "ListJobsRequest",
    "ListJobsResponse",
    "SearchJobsRequest",
    "SearchJobsResponse",
    "UpdateJobRequest",
    "JobView",
    "Tenant",
    "CreateTenantRequest",
    "DeleteTenantRequest",
    "GetTenantRequest",
    "ListTenantsRequest",
    "ListTenantsResponse",
    "UpdateTenantRequest",
)
