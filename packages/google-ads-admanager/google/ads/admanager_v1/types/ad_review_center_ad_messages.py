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

from google.ads.admanager_v1.types import (
    ad_review_center_ad_enums,
    exchange_syndication_product_enum,
)

__protobuf__ = proto.module(
    package="google.ads.admanager.v1",
    manifest={
        "AdReviewCenterAd",
    },
)


class AdReviewCenterAd(proto.Message):
    r"""Represents an ad that can be acted on or viewed in the Ad Review
    Center.
    [AdReviewCenterAd][google.ads.admanager.v1.AdReviewCenterAd].


    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        name (str):
            Identifier. The resource name of the AdReviewCenterAd.
            Format:
            ``networks/{network_code}/webProperties/{web_property_code}/adReviewCenterAds/{ad_review_center_ad_id}``
        ad_review_center_ad_id (str):
            Output only. ``AdReviewCenterAd`` ID.
        product_type (google.ads.admanager_v1.types.ExchangeSyndicationProductEnum.ExchangeSyndicationProduct):
            Output only. Specifies the
            ExchangeSyndicationProduct for this
            AdReviewCenterAd.
        status (google.ads.admanager_v1.types.AdReviewCenterAdStatusEnum.AdReviewCenterAdStatus):
            The status of the AdReviewCenterAd.
        preview_url (str):
            Output only. The preview URL that can be
            embedded or accessed directly which will present
            the rendered contents of the ad. (This URL
            expires 72 hours after being retrieved.).

            This field is a member of `oneof`_ ``_preview_url``.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    ad_review_center_ad_id: str = proto.Field(
        proto.STRING,
        number=2,
    )
    product_type: exchange_syndication_product_enum.ExchangeSyndicationProductEnum.ExchangeSyndicationProduct = proto.Field(
        proto.ENUM,
        number=3,
        enum=exchange_syndication_product_enum.ExchangeSyndicationProductEnum.ExchangeSyndicationProduct,
    )
    status: ad_review_center_ad_enums.AdReviewCenterAdStatusEnum.AdReviewCenterAdStatus = proto.Field(
        proto.ENUM,
        number=4,
        enum=ad_review_center_ad_enums.AdReviewCenterAdStatusEnum.AdReviewCenterAdStatus,
    )
    preview_url: str = proto.Field(
        proto.STRING,
        number=5,
        optional=True,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
