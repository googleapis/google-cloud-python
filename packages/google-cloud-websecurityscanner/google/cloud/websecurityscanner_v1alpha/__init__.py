# -*- coding: utf-8 -*-
# Copyright 2025 Google LLC
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
from google.cloud.websecurityscanner_v1alpha import gapic_version as package_version

__version__ = package_version.__version__


from .services.web_security_scanner import (
    WebSecurityScannerAsyncClient,
    WebSecurityScannerClient,
)
from .types.crawled_url import CrawledUrl
from .types.finding import Finding
from .types.finding_addon import (
    OutdatedLibrary,
    ViolatingResource,
    VulnerableHeaders,
    VulnerableParameters,
    Xss,
)
from .types.finding_type_stats import FindingTypeStats
from .types.scan_config import ScanConfig
from .types.scan_run import ScanRun
from .types.web_security_scanner import (
    CreateScanConfigRequest,
    DeleteScanConfigRequest,
    GetFindingRequest,
    GetScanConfigRequest,
    GetScanRunRequest,
    ListCrawledUrlsRequest,
    ListCrawledUrlsResponse,
    ListFindingsRequest,
    ListFindingsResponse,
    ListFindingTypeStatsRequest,
    ListFindingTypeStatsResponse,
    ListScanConfigsRequest,
    ListScanConfigsResponse,
    ListScanRunsRequest,
    ListScanRunsResponse,
    StartScanRunRequest,
    StopScanRunRequest,
    UpdateScanConfigRequest,
)

__all__ = (
    "WebSecurityScannerAsyncClient",
    "CrawledUrl",
    "CreateScanConfigRequest",
    "DeleteScanConfigRequest",
    "Finding",
    "FindingTypeStats",
    "GetFindingRequest",
    "GetScanConfigRequest",
    "GetScanRunRequest",
    "ListCrawledUrlsRequest",
    "ListCrawledUrlsResponse",
    "ListFindingTypeStatsRequest",
    "ListFindingTypeStatsResponse",
    "ListFindingsRequest",
    "ListFindingsResponse",
    "ListScanConfigsRequest",
    "ListScanConfigsResponse",
    "ListScanRunsRequest",
    "ListScanRunsResponse",
    "OutdatedLibrary",
    "ScanConfig",
    "ScanRun",
    "StartScanRunRequest",
    "StopScanRunRequest",
    "UpdateScanConfigRequest",
    "ViolatingResource",
    "VulnerableHeaders",
    "VulnerableParameters",
    "WebSecurityScannerClient",
    "Xss",
)
