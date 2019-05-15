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
"""Wrappers for protocol buffer enum types."""

import enum


class ScanConfig(object):
    class ExportToSecurityCommandCenter(enum.IntEnum):
        """
        Controls export of scan configurations and results to Cloud Security
        Command Center.

        Attributes:
          EXPORT_TO_SECURITY_COMMAND_CENTER_UNSPECIFIED (int): Use default, which is ENABLED.
          ENABLED (int): Export results of this scan to Cloud Security Command Center.
          DISABLED (int): Do not export results of this scan to Cloud Security Command Center.
        """

        EXPORT_TO_SECURITY_COMMAND_CENTER_UNSPECIFIED = 0
        ENABLED = 1
        DISABLED = 2

    class RiskLevel(enum.IntEnum):
        """
        Scan risk levels supported by Cloud Web Security Scanner. LOW impact
        scanning will minimize requests with the potential to modify data. To
        achieve the maximum scan coverage, NORMAL risk level is recommended.

        Attributes:
          RISK_LEVEL_UNSPECIFIED (int): Use default, which is NORMAL.
          NORMAL (int): Normal scanning (Recommended)
          LOW (int): Lower impact scanning
        """

        RISK_LEVEL_UNSPECIFIED = 0
        NORMAL = 1
        LOW = 2

    class TargetPlatform(enum.IntEnum):
        """
        Cloud platforms supported by Cloud Web Security Scanner.

        Attributes:
          TARGET_PLATFORM_UNSPECIFIED (int): The target platform is unknown. Requests with this enum value will be
          rejected with INVALID\_ARGUMENT error.
          APP_ENGINE (int): Google App Engine service.
          COMPUTE (int): Google Compute Engine service.
        """

        TARGET_PLATFORM_UNSPECIFIED = 0
        APP_ENGINE = 1
        COMPUTE = 2

    class UserAgent(enum.IntEnum):
        """
        Type of user agents used for scanning.

        Attributes:
          USER_AGENT_UNSPECIFIED (int): The user agent is unknown. Service will default to CHROME\_LINUX.
          CHROME_LINUX (int): Chrome on Linux. This is the service default if unspecified.
          CHROME_ANDROID (int): Chrome on Android.
          SAFARI_IPHONE (int): Safari on IPhone.
        """

        USER_AGENT_UNSPECIFIED = 0
        CHROME_LINUX = 1
        CHROME_ANDROID = 2
        SAFARI_IPHONE = 3


class ScanConfigError(object):
    class Code(enum.IntEnum):
        """
        Output only.
        Defines an error reason code.
        Next id: 43

        Attributes:
          CODE_UNSPECIFIED (int): There is no error.
          OK (int): There is no error.
          INTERNAL_ERROR (int): Indicates an internal server error.
          Please DO NOT USE THIS ERROR CODE unless the root cause is truly unknown.
          APPENGINE_API_BACKEND_ERROR (int): One of the seed URLs is an App Engine URL but we cannot validate the scan
          settings due to an App Engine API backend error.
          APPENGINE_API_NOT_ACCESSIBLE (int): One of the seed URLs is an App Engine URL but we cannot access the
          App Engine API to validate scan settings.
          APPENGINE_DEFAULT_HOST_MISSING (int): One of the seed URLs is an App Engine URL but the Default Host of the
          App Engine is not set.
          CANNOT_USE_GOOGLE_COM_ACCOUNT (int): Google corporate accounts can not be used for scanning.
          CANNOT_USE_OWNER_ACCOUNT (int): The account of the scan creator can not be used for scanning.
          COMPUTE_API_BACKEND_ERROR (int): This scan targets Compute Engine, but we cannot validate scan settings
          due to a Compute Engine API backend error.
          COMPUTE_API_NOT_ACCESSIBLE (int): This scan targets Compute Engine, but we cannot access the Compute Engine
          API to validate the scan settings.
          CUSTOM_LOGIN_URL_DOES_NOT_BELONG_TO_CURRENT_PROJECT (int): The Custom Login URL does not belong to the current project.
          CUSTOM_LOGIN_URL_MALFORMED (int): The Custom Login URL is malformed (can not be parsed).
          CUSTOM_LOGIN_URL_MAPPED_TO_NON_ROUTABLE_ADDRESS (int): The Custom Login URL is mapped to a non-routable IP address in DNS.
          CUSTOM_LOGIN_URL_MAPPED_TO_UNRESERVED_ADDRESS (int): The Custom Login URL is mapped to an IP address which is not reserved for
          the current project.
          CUSTOM_LOGIN_URL_HAS_NON_ROUTABLE_IP_ADDRESS (int): The Custom Login URL has a non-routable IP address.
          CUSTOM_LOGIN_URL_HAS_UNRESERVED_IP_ADDRESS (int): The Custom Login URL has an IP address which is not reserved for the
          current project.
          DUPLICATE_SCAN_NAME (int): Another scan with the same name (case-sensitive) already exists.
          INVALID_FIELD_VALUE (int): A field is set to an invalid value.
          FAILED_TO_AUTHENTICATE_TO_TARGET (int): There was an error trying to authenticate to the scan target.
          FINDING_TYPE_UNSPECIFIED (int): Finding type value is not specified in the list findings request.
          FORBIDDEN_TO_SCAN_COMPUTE (int): Scan targets Compute Engine, yet current project was not whitelisted for
          Google Compute Engine Scanning Alpha access.
          MALFORMED_FILTER (int): The supplied filter is malformed. For example, it can not be parsed, does
          not have a filter type in expression, or the same filter type appears
          more than once.
          MALFORMED_RESOURCE_NAME (int): The supplied resource name is malformed (can not be parsed).
          PROJECT_INACTIVE (int): The current project is not in an active state.
          REQUIRED_FIELD (int): A required field is not set.
          RESOURCE_NAME_INCONSISTENT (int): Project id, scanconfig id, scanrun id, or finding id are not consistent
          with each other in resource name.
          SCAN_ALREADY_RUNNING (int): The scan being requested to start is already running.
          SCAN_NOT_RUNNING (int): The scan that was requested to be stopped is not running.
          SEED_URL_DOES_NOT_BELONG_TO_CURRENT_PROJECT (int): One of the seed URLs does not belong to the current project.
          SEED_URL_MALFORMED (int): One of the seed URLs is malformed (can not be parsed).
          SEED_URL_MAPPED_TO_NON_ROUTABLE_ADDRESS (int): One of the seed URLs is mapped to a non-routable IP address in DNS.
          SEED_URL_MAPPED_TO_UNRESERVED_ADDRESS (int): One of the seed URLs is mapped to an IP address which is not reserved
          for the current project.
          SEED_URL_HAS_NON_ROUTABLE_IP_ADDRESS (int): One of the seed URLs has on-routable IP address.
          SEED_URL_HAS_UNRESERVED_IP_ADDRESS (int): One of the seed URLs has an IP address that is not reserved
          for the current project.
          SERVICE_ACCOUNT_NOT_CONFIGURED (int): The Cloud Security Scanner service account is not configured under the
          project.
          TOO_MANY_SCANS (int): A project has reached the maximum number of scans.
          UNABLE_TO_RESOLVE_PROJECT_INFO (int): Resolving the details of the current project fails.
          UNSUPPORTED_BLACKLIST_PATTERN_FORMAT (int): One or more blacklist patterns were in the wrong format.
          UNSUPPORTED_FILTER (int): The supplied filter is not supported.
          UNSUPPORTED_FINDING_TYPE (int): The supplied finding type is not supported. For example, we do not
          provide findings of the given finding type.
          UNSUPPORTED_URL_SCHEME (int): The URL scheme of one or more of the supplied URLs is not supported.
        """

        CODE_UNSPECIFIED = 0
        OK = 0
        INTERNAL_ERROR = 1
        APPENGINE_API_BACKEND_ERROR = 2
        APPENGINE_API_NOT_ACCESSIBLE = 3
        APPENGINE_DEFAULT_HOST_MISSING = 4
        CANNOT_USE_GOOGLE_COM_ACCOUNT = 6
        CANNOT_USE_OWNER_ACCOUNT = 7
        COMPUTE_API_BACKEND_ERROR = 8
        COMPUTE_API_NOT_ACCESSIBLE = 9
        CUSTOM_LOGIN_URL_DOES_NOT_BELONG_TO_CURRENT_PROJECT = 10
        CUSTOM_LOGIN_URL_MALFORMED = 11
        CUSTOM_LOGIN_URL_MAPPED_TO_NON_ROUTABLE_ADDRESS = 12
        CUSTOM_LOGIN_URL_MAPPED_TO_UNRESERVED_ADDRESS = 13
        CUSTOM_LOGIN_URL_HAS_NON_ROUTABLE_IP_ADDRESS = 14
        CUSTOM_LOGIN_URL_HAS_UNRESERVED_IP_ADDRESS = 15
        DUPLICATE_SCAN_NAME = 16
        INVALID_FIELD_VALUE = 18
        FAILED_TO_AUTHENTICATE_TO_TARGET = 19
        FINDING_TYPE_UNSPECIFIED = 20
        FORBIDDEN_TO_SCAN_COMPUTE = 21
        MALFORMED_FILTER = 22
        MALFORMED_RESOURCE_NAME = 23
        PROJECT_INACTIVE = 24
        REQUIRED_FIELD = 25
        RESOURCE_NAME_INCONSISTENT = 26
        SCAN_ALREADY_RUNNING = 27
        SCAN_NOT_RUNNING = 28
        SEED_URL_DOES_NOT_BELONG_TO_CURRENT_PROJECT = 29
        SEED_URL_MALFORMED = 30
        SEED_URL_MAPPED_TO_NON_ROUTABLE_ADDRESS = 31
        SEED_URL_MAPPED_TO_UNRESERVED_ADDRESS = 32
        SEED_URL_HAS_NON_ROUTABLE_IP_ADDRESS = 33
        SEED_URL_HAS_UNRESERVED_IP_ADDRESS = 35
        SERVICE_ACCOUNT_NOT_CONFIGURED = 36
        TOO_MANY_SCANS = 37
        UNABLE_TO_RESOLVE_PROJECT_INFO = 38
        UNSUPPORTED_BLACKLIST_PATTERN_FORMAT = 39
        UNSUPPORTED_FILTER = 40
        UNSUPPORTED_FINDING_TYPE = 41
        UNSUPPORTED_URL_SCHEME = 42


class ScanRun(object):
    class ExecutionState(enum.IntEnum):
        """
        Types of ScanRun execution state.

        Attributes:
          EXECUTION_STATE_UNSPECIFIED (int): Represents an invalid state caused by internal server error. This value
          should never be returned.
          QUEUED (int): The scan is waiting in the queue.
          SCANNING (int): The scan is in progress.
          FINISHED (int): The scan is either finished or stopped by user.
        """

        EXECUTION_STATE_UNSPECIFIED = 0
        QUEUED = 1
        SCANNING = 2
        FINISHED = 3

    class ResultState(enum.IntEnum):
        """
        Types of ScanRun result state.

        Attributes:
          RESULT_STATE_UNSPECIFIED (int): Default value. This value is returned when the ScanRun is not yet
          finished.
          SUCCESS (int): The scan finished without errors.
          ERROR (int): The scan finished with errors.
          KILLED (int): The scan was terminated by user.
        """

        RESULT_STATE_UNSPECIFIED = 0
        SUCCESS = 1
        ERROR = 2
        KILLED = 3


class ScanRunErrorTrace(object):
    class Code(enum.IntEnum):
        """
        Output only.
        Defines an error reason code.
        Next id: 7

        Attributes:
          CODE_UNSPECIFIED (int): Default value is never used.
          INTERNAL_ERROR (int): Indicates that the scan run failed due to an internal server error.
          SCAN_CONFIG_ISSUE (int): Indicates a scan configuration error, usually due to outdated ScanConfig
          settings, such as starting\_urls or the DNS configuration.
          AUTHENTICATION_CONFIG_ISSUE (int): Indicates an authentication error, usually due to outdated ScanConfig
          authentication settings.
          TIMED_OUT_WHILE_SCANNING (int): Indicates a scan operation timeout, usually caused by a very large site.
          TOO_MANY_REDIRECTS (int): Indicates that a scan encountered excessive redirects, either to
          authentication or some other page outside of the scan scope.
          TOO_MANY_HTTP_ERRORS (int): Indicates that a scan encountered numerous errors from the web site
          pages. When available, most\_common\_http\_error\_code field indicates
          the the most common HTTP error code encountered during the scan.
        """

        CODE_UNSPECIFIED = 0
        INTERNAL_ERROR = 1
        SCAN_CONFIG_ISSUE = 2
        AUTHENTICATION_CONFIG_ISSUE = 3
        TIMED_OUT_WHILE_SCANNING = 4
        TOO_MANY_REDIRECTS = 5
        TOO_MANY_HTTP_ERRORS = 6


class ScanRunWarningTrace(object):
    class Code(enum.IntEnum):
        """
        Output only.
        Defines a warning message code.
        Next id: 5

        Attributes:
          CODE_UNSPECIFIED (int): Default value is never used.
          INSUFFICIENT_CRAWL_RESULTS (int): Indicates that a scan discovered an unexpectedly low number of URLs. This
          is sometimes caused by complex navigation features or by using a single
          URL for numerous pages.
          TOO_MANY_CRAWL_RESULTS (int): Indicates that a scan discovered too many URLs to test, or excessive
          redundant URLs.
          TOO_MANY_FUZZ_TASKS (int): Indicates that too many tests have been generated for the scan. Customer
          should try reducing the number of starting URLs, increasing the QPS rate,
          or narrowing down the scope of the scan using the excluded patterns.
          BLOCKED_BY_IAP (int): Indicates that a scan is blocked by IAP.
        """

        CODE_UNSPECIFIED = 0
        INSUFFICIENT_CRAWL_RESULTS = 1
        TOO_MANY_CRAWL_RESULTS = 2
        TOO_MANY_FUZZ_TASKS = 3
        BLOCKED_BY_IAP = 4
