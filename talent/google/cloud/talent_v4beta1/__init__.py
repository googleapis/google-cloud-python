# -*- coding: utf-8 -*-
#
# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from __future__ import absolute_import

from google.cloud.talent_v4beta1 import types
from google.cloud.talent_v4beta1.gapic import application_service_client
from google.cloud.talent_v4beta1.gapic import company_service_client
from google.cloud.talent_v4beta1.gapic import completion_client
from google.cloud.talent_v4beta1.gapic import enums
from google.cloud.talent_v4beta1.gapic import event_service_client
from google.cloud.talent_v4beta1.gapic import job_service_client
from google.cloud.talent_v4beta1.gapic import profile_service_client
from google.cloud.talent_v4beta1.gapic import tenant_service_client


class ApplicationServiceClient(application_service_client.ApplicationServiceClient):
    __doc__ = application_service_client.ApplicationServiceClient.__doc__
    enums = enums


class CompanyServiceClient(company_service_client.CompanyServiceClient):
    __doc__ = company_service_client.CompanyServiceClient.__doc__
    enums = enums


class CompletionClient(completion_client.CompletionClient):
    __doc__ = completion_client.CompletionClient.__doc__
    enums = enums


class EventServiceClient(event_service_client.EventServiceClient):
    __doc__ = event_service_client.EventServiceClient.__doc__
    enums = enums


class JobServiceClient(job_service_client.JobServiceClient):
    __doc__ = job_service_client.JobServiceClient.__doc__
    enums = enums


class ProfileServiceClient(profile_service_client.ProfileServiceClient):
    __doc__ = profile_service_client.ProfileServiceClient.__doc__
    enums = enums


class TenantServiceClient(tenant_service_client.TenantServiceClient):
    __doc__ = tenant_service_client.TenantServiceClient.__doc__
    enums = enums


__all__ = (
    "enums",
    "types",
    "ApplicationServiceClient",
    "CompanyServiceClient",
    "CompletionClient",
    "EventServiceClient",
    "JobServiceClient",
    "ProfileServiceClient",
    "TenantServiceClient",
)
