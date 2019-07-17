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

from google.cloud.audit.proto.audit_log_pb2 import AuditLog
from google.cloud.audit.proto.audit_log_pb2 import AuthenticationInfo
from google.cloud.audit.proto.audit_log_pb2 import AuthorizationInfo
from google.cloud.audit.proto.audit_log_pb2 import RequestMetadata

# Update to account for moved module.
for message in (AuditLog, AuthenticationInfo, AuthorizationInfo, RequestMetadata):
    message.__module__ = "google.cloud.audit.proto.audit_log_pb2"


__all__ = ("AuditLog", "AuthenticationInfo", "AuthorizationInfo", "RequestMetadata")
