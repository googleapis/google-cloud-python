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

from .common import (
    TimestampRange,
    Location,
    RequestMetadata,
    ResponseMetadata,
    DeviceInfo,
    CustomAttribute,
    SpellingCorrection,
    CompensationInfo,
    BatchOperationMetadata,
    CompanySize,
    JobBenefit,
    DegreeType,
    EmploymentType,
    JobLevel,
    JobCategory,
    PostingRegion,
    Visibility,
    HtmlSanitization,
    CommuteMethod,
)
from .company import Company
from .company_service import (
    CreateCompanyRequest,
    GetCompanyRequest,
    UpdateCompanyRequest,
    DeleteCompanyRequest,
    ListCompaniesRequest,
    ListCompaniesResponse,
)
from .completion_service import (
    CompleteQueryRequest,
    CompleteQueryResponse,
)
from .event import (
    ClientEvent,
    JobEvent,
)
from .event_service import CreateClientEventRequest
from .filters import (
    JobQuery,
    LocationFilter,
    CompensationFilter,
    CommuteFilter,
)
from .histogram import (
    HistogramQuery,
    HistogramQueryResult,
)
from .job import Job
from .job_service import (
    CreateJobRequest,
    GetJobRequest,
    UpdateJobRequest,
    DeleteJobRequest,
    ListJobsRequest,
    ListJobsResponse,
    SearchJobsRequest,
    SearchJobsResponse,
    BatchCreateJobsRequest,
    BatchUpdateJobsRequest,
    BatchDeleteJobsRequest,
    JobResult,
    BatchCreateJobsResponse,
    BatchUpdateJobsResponse,
    BatchDeleteJobsResponse,
    JobView,
)
from .tenant import Tenant
from .tenant_service import (
    CreateTenantRequest,
    GetTenantRequest,
    UpdateTenantRequest,
    DeleteTenantRequest,
    ListTenantsRequest,
    ListTenantsResponse,
)

__all__ = (
    "TimestampRange",
    "Location",
    "RequestMetadata",
    "ResponseMetadata",
    "DeviceInfo",
    "CustomAttribute",
    "SpellingCorrection",
    "CompensationInfo",
    "BatchOperationMetadata",
    "CompanySize",
    "JobBenefit",
    "DegreeType",
    "EmploymentType",
    "JobLevel",
    "JobCategory",
    "PostingRegion",
    "Visibility",
    "HtmlSanitization",
    "CommuteMethod",
    "Company",
    "CreateCompanyRequest",
    "GetCompanyRequest",
    "UpdateCompanyRequest",
    "DeleteCompanyRequest",
    "ListCompaniesRequest",
    "ListCompaniesResponse",
    "CompleteQueryRequest",
    "CompleteQueryResponse",
    "ClientEvent",
    "JobEvent",
    "CreateClientEventRequest",
    "JobQuery",
    "LocationFilter",
    "CompensationFilter",
    "CommuteFilter",
    "HistogramQuery",
    "HistogramQueryResult",
    "Job",
    "CreateJobRequest",
    "GetJobRequest",
    "UpdateJobRequest",
    "DeleteJobRequest",
    "ListJobsRequest",
    "ListJobsResponse",
    "SearchJobsRequest",
    "SearchJobsResponse",
    "BatchCreateJobsRequest",
    "BatchUpdateJobsRequest",
    "BatchDeleteJobsRequest",
    "JobResult",
    "BatchCreateJobsResponse",
    "BatchUpdateJobsResponse",
    "BatchDeleteJobsResponse",
    "JobView",
    "Tenant",
    "CreateTenantRequest",
    "GetTenantRequest",
    "UpdateTenantRequest",
    "DeleteTenantRequest",
    "ListTenantsRequest",
    "ListTenantsResponse",
)
