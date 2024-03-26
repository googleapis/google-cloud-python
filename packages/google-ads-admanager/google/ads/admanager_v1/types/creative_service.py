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
from __future__ import annotations

from typing import MutableMapping, MutableSequence

from google.protobuf import timestamp_pb2  # type: ignore
import proto  # type: ignore

from google.ads.admanager_v1.types import (
    ad_partner_declaration as gaa_ad_partner_declaration,
)

__protobuf__ = proto.module(
    package="google.ads.admanager.v1",
    manifest={
        "Creative",
        "GetCreativeRequest",
        "ListCreativesRequest",
        "ListCreativesResponse",
    },
)


class Creative(proto.Message):
    r"""The Creative resource.

    Attributes:
        name (str):
            Identifier. The resource name of the Creative. Format:
            ``networks/{network_code}/creatives/{creative_id}``
        creative_id (int):
            Output only. ``Creative`` ID.
        display_name (str):
            Optional. Display name of the ``Creative``. This attribute
            has a maximum length of 255 characters.
        advertiser (str):
            Required. The resource name of the Company, which is of type
            Company.Type.ADVERTISER, to which this Creative belongs.
            Format: "networks/{network_code}/companies/{company_id}".
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The instant this Creative was
            last modified.
        preview_url (str):
            Output only. The URL of the creative for
            previewing the media.
        size_label (str):
            Output only. String representations of creative size. This
            field is temporarily available and will be deprecated when
            ``Creative.size`` becomes available.
        ad_partner_declaration (google.ads.admanager_v1.types.AdPartnerDeclaration):
            Optional. The Ad Partners associated with
            this creative. This is distinct from any
            associated companies that Google may detect
            programmatically.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    creative_id: int = proto.Field(
        proto.INT64,
        number=7,
    )
    display_name: str = proto.Field(
        proto.STRING,
        number=8,
    )
    advertiser: str = proto.Field(
        proto.STRING,
        number=2,
    )
    update_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=3,
        message=timestamp_pb2.Timestamp,
    )
    preview_url: str = proto.Field(
        proto.STRING,
        number=4,
    )
    size_label: str = proto.Field(
        proto.STRING,
        number=9,
    )
    ad_partner_declaration: gaa_ad_partner_declaration.AdPartnerDeclaration = (
        proto.Field(
            proto.MESSAGE,
            number=6,
            message=gaa_ad_partner_declaration.AdPartnerDeclaration,
        )
    )


class GetCreativeRequest(proto.Message):
    r"""Request object for GetCreative method.

    Attributes:
        name (str):
            Required. The resource name of the Creative. Format:
            ``networks/{network_code}/creatives/{creative_id}``
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class ListCreativesRequest(proto.Message):
    r"""Request object for ListCreatives method.

    Attributes:
        parent (str):
            Required. The parent, which owns this collection of
            Creatives. Format: networks/{network_code}
        page_size (int):
            Optional. The maximum number of Creatives to
            return. The service may return fewer than this
            value. If unspecified, at most 50 creatives will
            be returned. The maximum value is 1000; values
            above 1000 will be coerced to 1000.
        page_token (str):
            Optional. A page token, received from a previous
            ``ListCreatives`` call. Provide this to retrieve the
            subsequent page.

            When paginating, all other parameters provided to
            ``ListCreatives`` must match the call that provided the page
            token.
        filter (str):
            Optional. Expression to filter the response.
            See syntax details at
            https://developers.google.com/ad-manager/api/beta/filters
        order_by (str):
            Optional. Expression to specify sorting
            order. See syntax details at
            https://developers.google.com/ad-manager/api/beta/filters#order
        skip (int):
            Optional. Number of individual resources to
            skip while paginating.
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
    filter: str = proto.Field(
        proto.STRING,
        number=4,
    )
    order_by: str = proto.Field(
        proto.STRING,
        number=5,
    )
    skip: int = proto.Field(
        proto.INT32,
        number=6,
    )


class ListCreativesResponse(proto.Message):
    r"""Response object for ListCreativesRequest containing matching
    Creative resources.

    Attributes:
        creatives (MutableSequence[google.ads.admanager_v1.types.Creative]):
            The Creative from the specified network.
        next_page_token (str):
            A token, which can be sent as ``page_token`` to retrieve the
            next page. If this field is omitted, there are no subsequent
            pages.
        total_size (int):
            Total number of Creatives. If a filter was included in the
            request, this reflects the total number after the filtering
            is applied.

            ``total_size`` will not be calculated in the response unless
            it has been included in a response field mask. The response
            field mask can be provided to the method by using the URL
            parameter ``$fields`` or ``fields``, or by using the
            HTTP/gRPC header ``X-Goog-FieldMask``.

            For more information, see
            https://developers.google.com/ad-manager/api/beta/field-masks
    """

    @property
    def raw_page(self):
        return self

    creatives: MutableSequence["Creative"] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="Creative",
    )
    next_page_token: str = proto.Field(
        proto.STRING,
        number=2,
    )
    total_size: int = proto.Field(
        proto.INT32,
        number=3,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
