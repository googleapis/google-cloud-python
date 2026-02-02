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

import google.rpc.status_pb2 as status_pb2  # type: ignore
import google.type.interval_pb2 as interval_pb2  # type: ignore
import proto  # type: ignore

from google.ads.admanager_v1.types import (
    ad_review_center_ad_enums,
    ad_review_center_ad_messages,
)

__protobuf__ = proto.module(
    package="google.ads.admanager.v1",
    manifest={
        "SearchAdReviewCenterAdsRequest",
        "SearchAdReviewCenterAdsResponse",
        "BatchAllowAdReviewCenterAdsRequest",
        "BatchAllowAdReviewCenterAdsResponse",
        "BatchBlockAdReviewCenterAdsRequest",
        "BatchBlockAdReviewCenterAdsResponse",
        "BatchAdReviewCenterAdsOperationMetadata",
    },
)


class SearchAdReviewCenterAdsRequest(proto.Message):
    r"""Request object for ``SearchAdReviewCenterAds`` method.

    Attributes:
        parent (str):
            Required. The parent, which owns this collection of
            AdReviewCenterAds. Format:
            networks/{network_code}/webProperties/{web_property_code}

            Since a network can only have a single web property of each
            ``ExchangeSyndicationProduct``, you can use the
            ``ExchangeSyndicationProduct`` as an alias for the web
            property code:

            ``networks/{network_code}/webProperties/display``

            ``networks/{network_code}/webProperties/videoAndAudio``

            ``networks/{network_code}/webProperties/mobileApp``

            ``networks/{network_code}/webProperties/games``
        page_size (int):
            Optional. The maximum number of
            AdReviewCenterAds to return. The service may
            return fewer than this value. If unspecified, at
            most 50 AdReviewCenterAds will be returned. The
            maximum value is 1000; values greater than 1000
            will be coerced to 1000.
        page_token (str):
            Optional. The page token to fetch the next
            page of AdReviewCenterAds. This is the value
            returned from a previous Search request, or
            empty.
        status (google.ads.admanager_v1.types.AdReviewCenterAdStatusEnum.AdReviewCenterAdStatus):
            Optional. Only return ads with the given
            status.
        ad_review_center_ad_id (MutableSequence[str]):
            Optional. Only return ads with the given
            AdReviewCenterAd IDs. If provided, no other
            filter can be set (other than page size and page
            token).
        date_time_range (google.type.interval_pb2.Interval):
            Optional. If provided, only return ads that
            served within the given date range (inclusive).
            The  date range must be within the last 30 days.
            If not provided, the date range will be the last
            30 days.
        search_text (MutableSequence[str]):
            Optional. If provided, restrict the search to
            AdReviewCenterAds associated with the text (including any
            text on the ad or in the destination URL). If more than one
            value is provided, the search will combine them in a logical
            AND. For example, ['car', 'blue'] will match ads that
            contain both "car" and "blue", but not an ad that only
            contains "car".
        buyer_account_id (MutableSequence[int]):
            Optional. If provided, restrict the search to
            creatives belonging to one of the given Adx
            buyer account IDs. Only applicable to RTB
            creatives. Adx buyer account IDs can be found
            via the ProgrammaticBuyerService.
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
    status: ad_review_center_ad_enums.AdReviewCenterAdStatusEnum.AdReviewCenterAdStatus = proto.Field(
        proto.ENUM,
        number=4,
        enum=ad_review_center_ad_enums.AdReviewCenterAdStatusEnum.AdReviewCenterAdStatus,
    )
    ad_review_center_ad_id: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=5,
    )
    date_time_range: interval_pb2.Interval = proto.Field(
        proto.MESSAGE,
        number=6,
        message=interval_pb2.Interval,
    )
    search_text: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=7,
    )
    buyer_account_id: MutableSequence[int] = proto.RepeatedField(
        proto.INT64,
        number=8,
    )


class SearchAdReviewCenterAdsResponse(proto.Message):
    r"""Response object for ``SearchAdReviewCenterAds`` method.

    Attributes:
        ad_review_center_ads (MutableSequence[google.ads.admanager_v1.types.AdReviewCenterAd]):
            The AdReviewCenterAds that match the search
            request.
        next_page_token (str):
            A token, which can be sent as ``page_token`` to retrieve the
            next page. If this field is omitted, there are no subsequent
            pages.
    """

    @property
    def raw_page(self):
        return self

    ad_review_center_ads: MutableSequence[
        ad_review_center_ad_messages.AdReviewCenterAd
    ] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message=ad_review_center_ad_messages.AdReviewCenterAd,
    )
    next_page_token: str = proto.Field(
        proto.STRING,
        number=2,
    )


class BatchAllowAdReviewCenterAdsRequest(proto.Message):
    r"""Request object for ``BatchAllowAdReviewCenterAds`` method.

    Attributes:
        parent (str):
            Required. The parent, which owns this collection of
            AdReviewCenterAds. Format:
            networks/{network_code}/webProperties/{web_property_code}

            Since a network can only have a single web property of each
            ``ExchangeSyndicationProduct``, you can use the
            ``ExchangeSyndicationProduct`` as an alias for the web
            property code:

            ``networks/{network_code}/webProperties/display``

            ``networks/{network_code}/webProperties/videoAndAudio``

            ``networks/{network_code}/webProperties/mobileApp``

            ``networks/{network_code}/webProperties/games``
        names (MutableSequence[str]):
            Required. The resource names of the ``AdReviewCenterAd``\ s
            to allow. Format:
            ``networks/{network_code}/webProperties/{web_property_code}/adReviewCenterAds/{ad_review_center_ad_id}``
    """

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    names: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=2,
    )


class BatchAllowAdReviewCenterAdsResponse(proto.Message):
    r"""Response object for ``BatchAllowAdReviewCenterAds`` method."""


class BatchBlockAdReviewCenterAdsRequest(proto.Message):
    r"""Request object for ``BatchBlockAdReviewCenterAds`` method.

    Attributes:
        parent (str):
            Required. The parent, which owns this collection of
            AdReviewCenterAds. Format:
            networks/{network_code}/webProperties/{web_property_code}

            Since a network can only have a single web property of each
            ``ExchangeSyndicationProduct``, you can use the
            ``ExchangeSyndicationProduct`` as an alias for the web
            property code:

            ``networks/{network_code}/webProperties/display``

            ``networks/{network_code}/webProperties/videoAndAudio``

            ``networks/{network_code}/webProperties/mobileApp``

            ``networks/{network_code}/webProperties/games``
        names (MutableSequence[str]):
            Required. The resource names of the ``AdReviewCenterAd``\ s
            to block. Format:
            ``networks/{network_code}/webProperties/{web_property_code}/adReviewCenterAds/{ad_review_center_ad_id}``
    """

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    names: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=2,
    )


class BatchBlockAdReviewCenterAdsResponse(proto.Message):
    r"""Response object for ``BatchBlockAdReviewCenterAds`` method."""


class BatchAdReviewCenterAdsOperationMetadata(proto.Message):
    r"""Metadata object for ``BatchAllowAdReviewCenterAds`` and
    ``BatchBlockAdReviewCenterAds`` methods.

    Attributes:
        failed_requests (MutableMapping[int, google.rpc.status_pb2.Status]):
            The status of each failed request, keyed by
            the index of the corresponding request in the
            batch request.
    """

    failed_requests: MutableMapping[int, status_pb2.Status] = proto.MapField(
        proto.INT32,
        proto.MESSAGE,
        number=1,
        message=status_pb2.Status,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
