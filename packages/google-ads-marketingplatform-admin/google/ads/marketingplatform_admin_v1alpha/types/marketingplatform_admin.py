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

from google.ads.marketingplatform_admin_v1alpha.types import resources

__protobuf__ = proto.module(
    package="google.marketingplatform.admin.v1alpha",
    manifest={
        "AnalyticsServiceLevel",
        "GetOrganizationRequest",
        "ListAnalyticsAccountLinksRequest",
        "ListAnalyticsAccountLinksResponse",
        "CreateAnalyticsAccountLinkRequest",
        "DeleteAnalyticsAccountLinkRequest",
        "SetPropertyServiceLevelRequest",
        "SetPropertyServiceLevelResponse",
    },
)


class AnalyticsServiceLevel(proto.Enum):
    r"""Various levels of service for Google Analytics.

    Values:
        ANALYTICS_SERVICE_LEVEL_UNSPECIFIED (0):
            Service level unspecified.
        ANALYTICS_SERVICE_LEVEL_STANDARD (1):
            The standard version of Google Analytics.
        ANALYTICS_SERVICE_LEVEL_360 (2):
            The premium version of Google Analytics.
    """
    ANALYTICS_SERVICE_LEVEL_UNSPECIFIED = 0
    ANALYTICS_SERVICE_LEVEL_STANDARD = 1
    ANALYTICS_SERVICE_LEVEL_360 = 2


class GetOrganizationRequest(proto.Message):
    r"""Request message for GetOrganization RPC.

    Attributes:
        name (str):
            Required. The name of the Organization to retrieve. Format:
            organizations/{org_id}
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class ListAnalyticsAccountLinksRequest(proto.Message):
    r"""Request message for ListAnalyticsAccountLinks RPC.

    Attributes:
        parent (str):
            Required. The parent organization, which owns this
            collection of Analytics account links. Format:
            organizations/{org_id}
        page_size (int):
            Optional. The maximum number of Analytics
            account links to return in one call. The service
            may return fewer than this value.

            If unspecified, at most 50 Analytics account
            links will be returned. The maximum value is
            1000; values above 1000 will be coerced to 1000.
        page_token (str):
            Optional. A page token, received from a previous
            ListAnalyticsAccountLinks call. Provide this to retrieve the
            subsequent page.

            When paginating, all other parameters provided to
            ``ListAnalyticsAccountLinks`` must match the call that
            provided the page token.
    """

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    page_size: int = proto.Field(
        proto.INT32,
        number=2,
    )
    page_token: str = proto.Field(
        proto.STRING,
        number=3,
    )


class ListAnalyticsAccountLinksResponse(proto.Message):
    r"""Response message for ListAnalyticsAccountLinks RPC.

    Attributes:
        analytics_account_links (MutableSequence[google.ads.marketingplatform_admin_v1alpha.types.AnalyticsAccountLink]):
            Analytics account links in this organization.
        next_page_token (str):
            A token, which can be sent as ``page_token`` to retrieve the
            next page. If this field is omitted, there are no subsequent
            pages.
    """

    @property
    def raw_page(self):
        return self

    analytics_account_links: MutableSequence[
        resources.AnalyticsAccountLink
    ] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message=resources.AnalyticsAccountLink,
    )
    next_page_token: str = proto.Field(
        proto.STRING,
        number=2,
    )


class CreateAnalyticsAccountLinkRequest(proto.Message):
    r"""Request message for CreateAnalyticsAccountLink RPC.

    Attributes:
        parent (str):
            Required. The parent resource where this Analytics account
            link will be created. Format: organizations/{org_id}
        analytics_account_link (google.ads.marketingplatform_admin_v1alpha.types.AnalyticsAccountLink):
            Required. The Analytics account link to
            create.
    """

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    analytics_account_link: resources.AnalyticsAccountLink = proto.Field(
        proto.MESSAGE,
        number=2,
        message=resources.AnalyticsAccountLink,
    )


class DeleteAnalyticsAccountLinkRequest(proto.Message):
    r"""Request message for DeleteAnalyticsAccountLink RPC.

    Attributes:
        name (str):
            Required. The name of the Analytics account link to delete.
            Format:
            organizations/{org_id}/analyticsAccountLinks/{analytics_account_link_id}
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class SetPropertyServiceLevelRequest(proto.Message):
    r"""Request message for SetPropertyServiceLevel RPC.

    Attributes:
        analytics_account_link (str):
            Required. The parent AnalyticsAccountLink scope where this
            property is in. Format:
            organizations/{org_id}/analyticsAccountLinks/{analytics_account_link_id}
        analytics_property (str):
            Required. The Analytics property to change the ServiceLevel
            setting. This field is the name of the Google Analytics
            Admin API property resource.

            Format:
            analyticsadmin.googleapis.com/properties/{property_id}
        service_level (google.ads.marketingplatform_admin_v1alpha.types.AnalyticsServiceLevel):
            Required. The service level to set for this
            property.
    """

    analytics_account_link: str = proto.Field(
        proto.STRING,
        number=1,
    )
    analytics_property: str = proto.Field(
        proto.STRING,
        number=2,
    )
    service_level: "AnalyticsServiceLevel" = proto.Field(
        proto.ENUM,
        number=3,
        enum="AnalyticsServiceLevel",
    )


class SetPropertyServiceLevelResponse(proto.Message):
    r"""Response message for SetPropertyServiceLevel RPC."""


__all__ = tuple(sorted(__protobuf__.manifest))
