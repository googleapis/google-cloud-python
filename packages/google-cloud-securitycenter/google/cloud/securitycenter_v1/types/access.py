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
from typing import MutableMapping, MutableSequence

import proto  # type: ignore

__protobuf__ = proto.module(
    package="google.cloud.securitycenter.v1",
    manifest={
        "Access",
        "ServiceAccountDelegationInfo",
        "Geolocation",
    },
)


class Access(proto.Message):
    r"""Represents an access event.

    Attributes:
        principal_email (str):
            Associated email, such as "foo@google.com".

            The email address of the authenticated user (or service
            account on behalf of third party principal) making the
            request. For third party identity callers, the
            ``principal_subject`` field is populated instead of this
            field. For privacy reasons, the principal email address is
            sometimes redacted. For more information, see `Caller
            identities in audit
            logs <https://cloud.google.com/logging/docs/audit#user-id>`__.
        caller_ip (str):
            Caller's IP address, such as "1.1.1.1".
        caller_ip_geo (google.cloud.securitycenter_v1.types.Geolocation):
            The caller IP's geolocation, which identifies
            where the call came from.
        user_agent_family (str):
            What kind of user agent is associated, for
            example operating system shells, embedded or
            stand-alone applications, etc.
        service_name (str):
            This is the API service that the service
            account made a call to, e.g.
            "iam.googleapis.com".
        method_name (str):
            The method that the service account called,
            e.g. "SetIamPolicy".
        principal_subject (str):
            A string representing the principal_subject associated with
            the identity. As compared to ``principal_email``, supports
            principals that aren't associated with email addresses, such
            as third party principals. For most identities, the format
            will be
            ``principal://iam.googleapis.com/{identity pool name}/subjects/{subject}``
            except for some GKE identities (GKE_WORKLOAD, FREEFORM,
            GKE_HUB_WORKLOAD) that are still in the legacy format
            ``serviceAccount:{identity pool name}[{subject}]``
        service_account_key_name (str):
            The name of the service account key used to create or
            exchange credentials for authenticating the service account
            making the request. This is a scheme-less URI full resource
            name. For example:

            "//iam.googleapis.com/projects/{PROJECT_ID}/serviceAccounts/{ACCOUNT}/keys/{key}".
        service_account_delegation_info (MutableSequence[google.cloud.securitycenter_v1.types.ServiceAccountDelegationInfo]):
            Identity delegation history of an
            authenticated service account that makes the
            request. It contains information on the real
            authorities that try to access GCP resources by
            delegating on a service account. When multiple
            authorities are present, they are guaranteed to
            be sorted based on the original ordering of the
            identity delegation events.
        user_name (str):
            A string that represents the username of a
            user, user account, or other entity involved in
            the access event. What the entity is and what
            its role in the access event is depends on the
            finding that this field appears in. The entity
            is likely not an IAM principal, but could be a
            user that is logged into an operating system, if
            the finding is VM-related, or a user that is
            logged into some type of application that is
            involved in the access event.
    """

    principal_email: str = proto.Field(
        proto.STRING,
        number=1,
    )
    caller_ip: str = proto.Field(
        proto.STRING,
        number=2,
    )
    caller_ip_geo: "Geolocation" = proto.Field(
        proto.MESSAGE,
        number=3,
        message="Geolocation",
    )
    user_agent_family: str = proto.Field(
        proto.STRING,
        number=4,
    )
    service_name: str = proto.Field(
        proto.STRING,
        number=5,
    )
    method_name: str = proto.Field(
        proto.STRING,
        number=6,
    )
    principal_subject: str = proto.Field(
        proto.STRING,
        number=7,
    )
    service_account_key_name: str = proto.Field(
        proto.STRING,
        number=8,
    )
    service_account_delegation_info: MutableSequence[
        "ServiceAccountDelegationInfo"
    ] = proto.RepeatedField(
        proto.MESSAGE,
        number=9,
        message="ServiceAccountDelegationInfo",
    )
    user_name: str = proto.Field(
        proto.STRING,
        number=11,
    )


class ServiceAccountDelegationInfo(proto.Message):
    r"""Identity delegation history of an authenticated service
    account.

    Attributes:
        principal_email (str):
            The email address of a Google account.
        principal_subject (str):
            A string representing the principal_subject associated with
            the identity. As compared to ``principal_email``, supports
            principals that aren't associated with email addresses, such
            as third party principals. For most identities, the format
            will be
            ``principal://iam.googleapis.com/{identity pool name}/subjects/{subject}``
            except for some GKE identities (GKE_WORKLOAD, FREEFORM,
            GKE_HUB_WORKLOAD) that are still in the legacy format
            ``serviceAccount:{identity pool name}[{subject}]``
    """

    principal_email: str = proto.Field(
        proto.STRING,
        number=1,
    )
    principal_subject: str = proto.Field(
        proto.STRING,
        number=2,
    )


class Geolocation(proto.Message):
    r"""Represents a geographical location for a given access.

    Attributes:
        region_code (str):
            A CLDR.
    """

    region_code: str = proto.Field(
        proto.STRING,
        number=1,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
