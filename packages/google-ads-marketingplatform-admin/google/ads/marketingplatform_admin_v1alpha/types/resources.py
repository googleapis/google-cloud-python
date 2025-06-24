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
from __future__ import annotations

from typing import MutableMapping, MutableSequence

import proto  # type: ignore

__protobuf__ = proto.module(
    package="google.marketingplatform.admin.v1alpha",
    manifest={
        "LinkVerificationState",
        "Organization",
        "AnalyticsAccountLink",
    },
)


class LinkVerificationState(proto.Enum):
    r"""The verification state of the link between a product account
    and a GMP organization.

    Values:
        LINK_VERIFICATION_STATE_UNSPECIFIED (0):
            The link state is unknown.
        LINK_VERIFICATION_STATE_VERIFIED (1):
            The link is established.
        LINK_VERIFICATION_STATE_NOT_VERIFIED (2):
            The link is requested, but hasn't been
            approved by the product account admin.
    """
    LINK_VERIFICATION_STATE_UNSPECIFIED = 0
    LINK_VERIFICATION_STATE_VERIFIED = 1
    LINK_VERIFICATION_STATE_NOT_VERIFIED = 2


class Organization(proto.Message):
    r"""A resource message representing a Google Marketing Platform
    organization.

    Attributes:
        name (str):
            Identifier. The resource name of the GMP organization.
            Format: organizations/{org_id}
        display_name (str):
            The human-readable name for the organization.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    display_name: str = proto.Field(
        proto.STRING,
        number=2,
    )


class AnalyticsAccountLink(proto.Message):
    r"""A resource message representing the link between a Google
    Analytics account and a Google Marketing Platform organization.

    Attributes:
        name (str):
            Identifier. Resource name of this AnalyticsAccountLink. Note
            the resource ID is the same as the ID of the Analtyics
            account.

            Format:
            organizations/{org_id}/analyticsAccountLinks/{analytics_account_link_id}
            Example: "organizations/xyz/analyticsAccountLinks/1234".
        analytics_account (str):
            Required. Immutable. The resource name of the AnalyticsAdmin
            API account. The account ID will be used as the ID of this
            AnalyticsAccountLink resource, which will become the final
            component of the resource name.

            Format: analyticsadmin.googleapis.com/accounts/{account_id}
        display_name (str):
            Output only. The human-readable name for the
            Analytics account.
        link_verification_state (google.ads.marketingplatform_admin_v1alpha.types.LinkVerificationState):
            Output only. The verification state of the
            link between the Analytics account and the
            parent organization.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    analytics_account: str = proto.Field(
        proto.STRING,
        number=2,
    )
    display_name: str = proto.Field(
        proto.STRING,
        number=3,
    )
    link_verification_state: "LinkVerificationState" = proto.Field(
        proto.ENUM,
        number=4,
        enum="LinkVerificationState",
    )


__all__ = tuple(sorted(__protobuf__.manifest))
