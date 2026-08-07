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

from typing import ClassVar as _ClassVar

from google.protobuf import descriptor as _descriptor
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper

ACCESS_TOKEN_EXPIRED: ErrorReason
ACCESS_TOKEN_SCOPE_INSUFFICIENT: ErrorReason
ACCESS_TOKEN_TYPE_UNSUPPORTED: ErrorReason
ACCOUNT_STATE_INVALID: ErrorReason
ACCOUNT_TYPE_UNSUPPORTED: ErrorReason
API_KEY_ANDROID_APP_BLOCKED: ErrorReason
API_KEY_HTTP_REFERRER_BLOCKED: ErrorReason
API_KEY_INVALID: ErrorReason
API_KEY_IOS_APP_BLOCKED: ErrorReason
API_KEY_IP_ADDRESS_BLOCKED: ErrorReason
API_KEY_SERVICE_BLOCKED: ErrorReason
BILLING_DISABLED: ErrorReason
CONSUMER_INVALID: ErrorReason
CONSUMER_SUSPENDED: ErrorReason
CREDENTIALS_MISSING: ErrorReason
CREDENTIAL_ANDROID_APP_INVALID: ErrorReason
CREDENTIAL_TYPE_UNSUPPORTED: ErrorReason
DESCRIPTOR: _descriptor.FileDescriptor
EMULATOR_QUOTA_EXCEEDED: ErrorReason
ENDPOINT_USAGE_RESTRICTION_VIOLATED: ErrorReason
ERROR_REASON_UNSPECIFIED: ErrorReason
GCP_SUSPENDED: ErrorReason
IAM_PERMISSION_DENIED: ErrorReason
JWT_TOKEN_INVALID: ErrorReason
LOCATION_ORG_POLICY_VIOLATED: ErrorReason
LOCATION_POLICY_VIOLATED: ErrorReason
LOCATION_TAX_POLICY_VIOLATED: ErrorReason
MCP_SERVER_DISABLED: ErrorReason
MISSING_ORIGIN: ErrorReason
ORG_RESTRICTION_HEADER_INVALID: ErrorReason
ORG_RESTRICTION_VIOLATION: ErrorReason
OVERLOADED_CREDENTIALS: ErrorReason
RATE_LIMIT_EXCEEDED: ErrorReason
RESOURCE_PROJECT_INVALID: ErrorReason
RESOURCE_QUOTA_EXCEEDED: ErrorReason
RESOURCE_USAGE_RESTRICTION_VIOLATED: ErrorReason
SECURITY_POLICY_VIOLATED: ErrorReason
SERVICE_DISABLED: ErrorReason
SERVICE_NOT_VISIBLE: ErrorReason
SESSION_COOKIE_INVALID: ErrorReason
SYSTEM_PARAMETER_UNSUPPORTED: ErrorReason
TLS_CIPHER_RESTRICTION_VIOLATED: ErrorReason
TLS_ORG_POLICY_VIOLATED: ErrorReason
USER_BLOCKED_BY_ADMIN: ErrorReason
USER_PROJECT_DENIED: ErrorReason

class ErrorReason(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
