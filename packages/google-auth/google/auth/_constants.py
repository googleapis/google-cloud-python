# Copyright 2026 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Shared constants."""

_SERVICE_ACCOUNT_REGIONAL_ACCESS_BOUNDARY_LOOKUP_ENDPOINT = "https://iamcredentials.googleapis.com/v1/projects/-/serviceAccounts/{service_account_email}/allowedLocations"
_WORKFORCE_POOL_REGIONAL_ACCESS_BOUNDARY_LOOKUP_ENDPOINT = "https://iamcredentials.googleapis.com/v1/locations/global/workforcePools/{pool_id}/allowedLocations"
_WORKLOAD_IDENTITY_POOL_REGIONAL_ACCESS_BOUNDARY_LOOKUP_ENDPOINT = "https://iamcredentials.googleapis.com/v1/projects/{project_number}/locations/global/workloadIdentityPools/{pool_id}/allowedLocations"
