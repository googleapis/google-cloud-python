# -*- coding: utf-8 -*-
# Copyright 2022 Google LLC
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
    package="google.cloud.securitycenter.v1",
    manifest={
        "Access",
        "Geolocation",
    },
)


class Access(proto.Message):
    r"""Represents an access event.

    Attributes:
        principal_email (str):
            Associated email, such as "foo@google.com".
        caller_ip (str):
            Caller's IP address, such as "1.1.1.1".
        caller_ip_geo (google.cloud.securitycenter_v1.types.Geolocation):
            The caller IP's geolocation, which identifies
            where the call came from.
        user_agent_family (str):
            What kind of user agent is associated, e.g.
            operating system shells, embedded or stand-alone
            applications, etc.
        service_name (str):
            This is the API service that the service
            account made a call to, e.g.
            "iam.googleapis.com".
        method_name (str):
            The method that the service account called,
            e.g. "SetIamPolicy".
    """

    principal_email = proto.Field(
        proto.STRING,
        number=1,
    )
    caller_ip = proto.Field(
        proto.STRING,
        number=2,
    )
    caller_ip_geo = proto.Field(
        proto.MESSAGE,
        number=3,
        message="Geolocation",
    )
    user_agent_family = proto.Field(
        proto.STRING,
        number=4,
    )
    service_name = proto.Field(
        proto.STRING,
        number=5,
    )
    method_name = proto.Field(
        proto.STRING,
        number=6,
    )


class Geolocation(proto.Message):
    r"""Represents a geographical location for a given access.

    Attributes:
        region_code (str):
            A CLDR.
    """

    region_code = proto.Field(
        proto.STRING,
        number=1,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
