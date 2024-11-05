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
from google.cloud.websecurityscanner_v1 import gapic_version as package_version

__version__ = package_version.__version__


from .services.web_security_scanner import WebSecurityScannerClient
from .services.web_security_scanner import WebSecurityScannerAsyncClient

from .types.crawled_url import CrawledUrl
from .types.finding import Finding
from .types.finding_addon import Form
from .types.finding_addon import OutdatedLibrary
from .types.finding_addon import ViolatingResource
from .types.finding_addon import VulnerableHeaders
from .types.finding_addon import VulnerableParameters
from .types.finding_addon import Xss
from .types.finding_addon import Xxe
from .types.finding_type_stats import FindingTypeStats
from .types.scan_config import ScanConfig
from .types.scan_config_error import ScanConfigError
from .types.scan_run import ScanRun
from .types.scan_run_error_trace import ScanRunErrorTrace
from .types.scan_run_log import ScanRunLog
from .types.scan_run_warning_trace import ScanRunWarningTrace
from .types.web_security_scanner import CreateScanConfigRequest
from .types.web_security_scanner import DeleteScanConfigRequest
from .types.web_security_scanner import GetFindingRequest
from .types.web_security_scanner import GetScanConfigRequest
from .types.web_security_scanner import GetScanRunRequest
from .types.web_security_scanner import ListCrawledUrlsRequest
from .types.web_security_scanner import ListCrawledUrlsResponse
from .types.web_security_scanner import ListFindingsRequest
from .types.web_security_scanner import ListFindingsResponse
from .types.web_security_scanner import ListFindingTypeStatsRequest
from .types.web_security_scanner import ListFindingTypeStatsResponse
from .types.web_security_scanner import ListScanConfigsRequest
from .types.web_security_scanner import ListScanConfigsResponse
from .types.web_security_scanner import ListScanRunsRequest
from .types.web_security_scanner import ListScanRunsResponse
from .types.web_security_scanner import StartScanRunRequest
from .types.web_security_scanner import StopScanRunRequest
from .types.web_security_scanner import UpdateScanConfigRequest

__all__ = (
    'WebSecurityScannerAsyncClient',
'CrawledUrl',
'CreateScanConfigRequest',
'DeleteScanConfigRequest',
'Finding',
'FindingTypeStats',
'Form',
'GetFindingRequest',
'GetScanConfigRequest',
'GetScanRunRequest',
'ListCrawledUrlsRequest',
'ListCrawledUrlsResponse',
'ListFindingTypeStatsRequest',
'ListFindingTypeStatsResponse',
'ListFindingsRequest',
'ListFindingsResponse',
'ListScanConfigsRequest',
'ListScanConfigsResponse',
'ListScanRunsRequest',
'ListScanRunsResponse',
'OutdatedLibrary',
'ScanConfig',
'ScanConfigError',
'ScanRun',
'ScanRunErrorTrace',
'ScanRunLog',
'ScanRunWarningTrace',
'StartScanRunRequest',
'StopScanRunRequest',
'UpdateScanConfigRequest',
'ViolatingResource',
'VulnerableHeaders',
'VulnerableParameters',
'WebSecurityScannerClient',
'Xss',
'Xxe',
)
