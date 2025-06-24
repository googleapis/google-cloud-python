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

from google.ads.admanager_v1.types import ad_unit_messages

__protobuf__ = proto.module(
    package="google.ads.admanager.v1",
    manifest={
        "GetAdUnitRequest",
        "ListAdUnitsRequest",
        "ListAdUnitsResponse",
        "ListAdUnitSizesRequest",
        "ListAdUnitSizesResponse",
    },
)


class GetAdUnitRequest(proto.Message):
    r"""Request object for GetAdUnit method.

    Attributes:
        name (str):
            Required. The resource name of the AdUnit. Format:
            ``networks/{network_code}/adUnits/{ad_unit_id}``
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class ListAdUnitsRequest(proto.Message):
    r"""Request object for ListAdUnits method.

    Attributes:
        parent (str):
            Required. The parent, which owns this collection of AdUnits.
            Format: ``networks/{network_code}``
        page_size (int):
            Optional. The maximum number of AdUnits to
            return. The service may return fewer than this
            value. If unspecified, at most 50 ad units will
            be returned. The maximum value is 1000; values
            above 1000 will be coerced to 1000.
        page_token (str):
            Optional. A page token, received from a previous
            ``ListAdUnits`` call. Provide this to retrieve the
            subsequent page.

            When paginating, all other parameters provided to
            ``ListAdUnits`` must match the call that provided the page
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


class ListAdUnitsResponse(proto.Message):
    r"""Response object for ListAdUnitsRequest containing matching
    AdUnit resources.

    Attributes:
        ad_units (MutableSequence[google.ads.admanager_v1.types.AdUnit]):
            The AdUnit from the specified network.
        next_page_token (str):
            A token, which can be sent as ``page_token`` to retrieve the
            next page. If this field is omitted, there are no subsequent
            pages.
        total_size (int):
            Total number of AdUnits. If a filter was included in the
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

    ad_units: MutableSequence[ad_unit_messages.AdUnit] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message=ad_unit_messages.AdUnit,
    )
    next_page_token: str = proto.Field(
        proto.STRING,
        number=2,
    )
    total_size: int = proto.Field(
        proto.INT32,
        number=3,
    )


class ListAdUnitSizesRequest(proto.Message):
    r"""Request object for ListAdUnitSizes method.

    Attributes:
        parent (str):
            Required. The parent, which owns this collection of
            AdUnitSizes. Format: ``networks/{network_code}``
        page_size (int):
            Optional. The maximum number of AdUnitSizes
            to return. The service may return fewer than
            this value. If unspecified, at most 50 ad unit
            sizes will be returned. The maximum value is
            1000; values above 1000 will be coerced to 1000.
        page_token (str):
            Optional. A page token, received from a previous
            ``ListAdUnitSizes`` call. Provide this to retrieve the
            subsequent page.

            When paginating, all other parameters provided to
            ``ListAdUnitSizes`` must match the call that provided the
            page token.
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


class ListAdUnitSizesResponse(proto.Message):
    r"""Response object for ListAdUnitSizesRequest containing
    matching AdUnitSizes.

    Attributes:
        ad_unit_sizes (MutableSequence[google.ads.admanager_v1.types.AdUnitSize]):
            The AdUnitSizes from the specified network.
        next_page_token (str):
            A token, which can be sent as ``page_token`` to retrieve the
            next page. If this field is omitted, there are no subsequent
            pages.
        total_size (int):
            Total number of AdUnitSizes. If a filter was included in the
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

    ad_unit_sizes: MutableSequence[ad_unit_messages.AdUnitSize] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message=ad_unit_messages.AdUnitSize,
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
