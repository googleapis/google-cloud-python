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

from google.rpc import status_pb2  # type: ignore


__protobuf__ = proto.module(
    package="google.api.servicecontrol.v1", manifest={"CheckError",},
)


class CheckError(proto.Message):
    r"""Defines the errors to be returned in
    [google.api.servicecontrol.v1.CheckResponse.check_errors][google.api.servicecontrol.v1.CheckResponse.check_errors].

    Attributes:
        code (google.cloud.servicecontrol_v1.types.CheckError.Code):
            The error code.
        subject (str):
            Subject to whom this error applies. See the
            specific code enum for more details on this
            field. For example:
            - "project:<project-id or project-number>"
            - "folder:<folder-id>"
            - "organization:<organization-id>".
        detail (str):
            Free-form text providing details on the error
            cause of the error.
        status (google.rpc.status_pb2.Status):
            Contains public information about the check error. If
            available, ``status.code`` will be non zero and client can
            propagate it out as public error.
    """

    class Code(proto.Enum):
        r"""Error codes for Check responses."""
        ERROR_CODE_UNSPECIFIED = 0
        NOT_FOUND = 5
        PERMISSION_DENIED = 7
        RESOURCE_EXHAUSTED = 8
        SERVICE_NOT_ACTIVATED = 104
        BILLING_DISABLED = 107
        PROJECT_DELETED = 108
        PROJECT_INVALID = 114
        CONSUMER_INVALID = 125
        IP_ADDRESS_BLOCKED = 109
        REFERER_BLOCKED = 110
        CLIENT_APP_BLOCKED = 111
        API_TARGET_BLOCKED = 122
        API_KEY_INVALID = 105
        API_KEY_EXPIRED = 112
        API_KEY_NOT_FOUND = 113
        INVALID_CREDENTIAL = 123
        NAMESPACE_LOOKUP_UNAVAILABLE = 300
        SERVICE_STATUS_UNAVAILABLE = 301
        BILLING_STATUS_UNAVAILABLE = 302
        CLOUD_RESOURCE_MANAGER_BACKEND_UNAVAILABLE = 305

    code = proto.Field(proto.ENUM, number=1, enum=Code,)
    subject = proto.Field(proto.STRING, number=4,)
    detail = proto.Field(proto.STRING, number=2,)
    status = proto.Field(proto.MESSAGE, number=3, message=status_pb2.Status,)


__all__ = tuple(sorted(__protobuf__.manifest))
