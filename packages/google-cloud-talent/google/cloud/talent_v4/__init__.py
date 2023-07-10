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
from google.cloud.talent_v4 import gapic_version as package_version

__version__ = package_version.__version__


from .services.company_service import CompanyServiceAsyncClient, CompanyServiceClient
from .services.completion import CompletionAsyncClient, CompletionClient
from .services.event_service import EventServiceAsyncClient, EventServiceClient
from .services.job_service import JobServiceAsyncClient, JobServiceClient
from .services.tenant_service import TenantServiceAsyncClient, TenantServiceClient
from .types.common import (
    BatchOperationMetadata,
    CommuteMethod,
    CompanySize,
    CompensationInfo,
    CustomAttribute,
    DegreeType,
    DeviceInfo,
    EmploymentType,
    HtmlSanitization,
    JobBenefit,
    JobCategory,
    JobLevel,
    Location,
    PostingRegion,
    RequestMetadata,
    ResponseMetadata,
    SpellingCorrection,
    TimestampRange,
    Visibility,
)
from .types.company import Company
from .types.company_service import (
    CreateCompanyRequest,
    DeleteCompanyRequest,
    GetCompanyRequest,
    ListCompaniesRequest,
    ListCompaniesResponse,
    UpdateCompanyRequest,
)
from .types.completion_service import CompleteQueryRequest, CompleteQueryResponse
from .types.event import ClientEvent, JobEvent
from .types.event_service import CreateClientEventRequest
from .types.filters import CommuteFilter, CompensationFilter, JobQuery, LocationFilter
from .types.histogram import HistogramQuery, HistogramQueryResult
from .types.job import Job
from .types.job_service import (
    BatchCreateJobsRequest,
    BatchCreateJobsResponse,
    BatchDeleteJobsRequest,
    BatchDeleteJobsResponse,
    BatchUpdateJobsRequest,
    BatchUpdateJobsResponse,
    CreateJobRequest,
    DeleteJobRequest,
    GetJobRequest,
    JobResult,
    JobView,
    ListJobsRequest,
    ListJobsResponse,
    SearchJobsRequest,
    SearchJobsResponse,
    UpdateJobRequest,
)
from .types.tenant import Tenant
from .types.tenant_service import (
    CreateTenantRequest,
    DeleteTenantRequest,
    GetTenantRequest,
    ListTenantsRequest,
    ListTenantsResponse,
    UpdateTenantRequest,
)

__all__ = (
    "CompanyServiceAsyncClient",
    "CompletionAsyncClient",
    "EventServiceAsyncClient",
    "JobServiceAsyncClient",
    "TenantServiceAsyncClient",
    "BatchCreateJobsRequest",
    "BatchCreateJobsResponse",
    "BatchDeleteJobsRequest",
    "BatchDeleteJobsResponse",
    "BatchOperationMetadata",
    "BatchUpdateJobsRequest",
    "BatchUpdateJobsResponse",
    "ClientEvent",
    "CommuteFilter",
    "CommuteMethod",
    "Company",
    "CompanyServiceClient",
    "CompanySize",
    "CompensationFilter",
    "CompensationInfo",
    "CompleteQueryRequest",
    "CompleteQueryResponse",
    "CompletionClient",
    "CreateClientEventRequest",
    "CreateCompanyRequest",
    "CreateJobRequest",
    "CreateTenantRequest",
    "CustomAttribute",
    "DegreeType",
    "DeleteCompanyRequest",
    "DeleteJobRequest",
    "DeleteTenantRequest",
    "DeviceInfo",
    "EmploymentType",
    "EventServiceClient",
    "GetCompanyRequest",
    "GetJobRequest",
    "GetTenantRequest",
    "HistogramQuery",
    "HistogramQueryResult",
    "HtmlSanitization",
    "Job",
    "JobBenefit",
    "JobCategory",
    "JobEvent",
    "JobLevel",
    "JobQuery",
    "JobResult",
    "JobServiceClient",
    "JobView",
    "ListCompaniesRequest",
    "ListCompaniesResponse",
    "ListJobsRequest",
    "ListJobsResponse",
    "ListTenantsRequest",
    "ListTenantsResponse",
    "Location",
    "LocationFilter",
    "PostingRegion",
    "RequestMetadata",
    "ResponseMetadata",
    "SearchJobsRequest",
    "SearchJobsResponse",
    "SpellingCorrection",
    "Tenant",
    "TenantServiceClient",
    "TimestampRange",
    "UpdateCompanyRequest",
    "UpdateJobRequest",
    "UpdateTenantRequest",
    "Visibility",
)
