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
import proto  # type: ignore


__protobuf__ = proto.module(
    package="google.cloud.websecurityscanner.v1beta", manifest={"ScanConfigError",},
)


class ScanConfigError(proto.Message):
    r"""Defines a custom error message used by CreateScanConfig and
    UpdateScanConfig APIs when scan configuration validation fails.
    It is also reported as part of a ScanRunErrorTrace message if
    scan validation fails due to a scan configuration error.

    Attributes:
        code (google.cloud.websecurityscanner_v1beta.types.ScanConfigError.Code):
            Indicates the reason code for a configuration
            failure.
        field_name (str):
            Indicates the full name of the ScanConfig field that
            triggers this error, for example "scan_config.max_qps". This
            field is provided for troubleshooting purposes only and its
            actual value can change in the future.
    """

    class Code(proto.Enum):
        r"""Output only.
        Defines an error reason code.
        Next id: 44
        """
        _pb_options = {"allow_alias": True}
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
        FORBIDDEN_UPDATE_TO_MANAGED_SCAN = 43
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

    code = proto.Field(proto.ENUM, number=1, enum=Code,)
    field_name = proto.Field(proto.STRING, number=2,)


__all__ = tuple(sorted(__protobuf__.manifest))
