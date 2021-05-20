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


__protobuf__ = proto.module(
    package="google.cloud.retail.v2",
    manifest={"CustomAttribute", "Image", "PriceInfo", "UserInfo",},
)


class CustomAttribute(proto.Message):
    r"""A custom attribute that is not explicitly modeled in
    [Product][google.cloud.retail.v2.Product]].

    Attributes:
        text (Sequence[str]):
            The textual values of this custom attribute. For example,
            ``["yellow", "green"]`` when the key is "color".

            At most 400 values are allowed. Empty values are not
            allowed. Each value must be a UTF-8 encoded string with a
            length limit of 256 characters. Otherwise, an
            INVALID_ARGUMENT error is returned.

            Exactly one of
            [text][google.cloud.retail.v2.CustomAttribute.text] or
            [numbers][google.cloud.retail.v2.CustomAttribute.numbers]
            should be set. Otherwise, an INVALID_ARGUMENT error is
            returned.
        numbers (Sequence[float]):
            The numerical values of this custom attribute. For example,
            ``[2.3, 15.4]`` when the key is "lengths_cm".

            At most 400 values are allowed.Otherwise, an
            INVALID_ARGUMENT error is returned.

            Exactly one of
            [text][google.cloud.retail.v2.CustomAttribute.text] or
            [numbers][google.cloud.retail.v2.CustomAttribute.numbers]
            should be set. Otherwise, an INVALID_ARGUMENT error is
            returned.
    """

    text = proto.RepeatedField(proto.STRING, number=1,)
    numbers = proto.RepeatedField(proto.DOUBLE, number=2,)


class Image(proto.Message):
    r"""[Product][google.cloud.retail.v2.Product] thumbnail/detail image.
    Attributes:
        uri (str):
            Required. URI of the image.

            This field must be a valid UTF-8 encoded URI with a length
            limit of 5,000 characters. Otherwise, an INVALID_ARGUMENT
            error is returned.

            Google Merchant Center property
            `image_link <https://support.google.com/merchants/answer/6324350>`__.
            Schema.org property
            `Product.image <https://schema.org/image>`__.
        height (int):
            Height of the image in number of pixels.

            This field must be nonnegative. Otherwise, an
            INVALID_ARGUMENT error is returned.
        width (int):
            Width of the image in number of pixels.

            This field must be nonnegative. Otherwise, an
            INVALID_ARGUMENT error is returned.
    """

    uri = proto.Field(proto.STRING, number=1,)
    height = proto.Field(proto.INT32, number=2,)
    width = proto.Field(proto.INT32, number=3,)


class PriceInfo(proto.Message):
    r"""The price information of a
    [Product][google.cloud.retail.v2.Product].

    Attributes:
        currency_code (str):
            The 3-letter currency code defined in `ISO
            4217 <https://www.iso.org/iso-4217-currency-codes.html>`__.

            If this field is an unrecognizable currency code, an
            INVALID_ARGUMENT error is returned.
        price (float):
            Price of the product.

            Google Merchant Center property
            `price <https://support.google.com/merchants/answer/6324371>`__.
            Schema.org property
            `Offer.priceSpecification <https://schema.org/priceSpecification>`__.
        original_price (float):
            Price of the product without any discount. If zero, by
            default set to be the
            [price][google.cloud.retail.v2.PriceInfo.price].
        cost (float):
            The costs associated with the sale of a particular product.
            Used for gross profit reporting.

            -  Profit = [price][google.cloud.retail.v2.PriceInfo.price]
               - [cost][google.cloud.retail.v2.PriceInfo.cost]

            Google Merchant Center property
            `cost_of_goods_sold <https://support.google.com/merchants/answer/9017895>`__.
    """

    currency_code = proto.Field(proto.STRING, number=1,)
    price = proto.Field(proto.FLOAT, number=2,)
    original_price = proto.Field(proto.FLOAT, number=3,)
    cost = proto.Field(proto.FLOAT, number=4,)


class UserInfo(proto.Message):
    r"""Information of an end user.
    Attributes:
        user_id (str):
            Highly recommended for logged-in users. Unique identifier
            for logged-in user, such as a user name.

            The field must be a UTF-8 encoded string with a length limit
            of 128 characters. Otherwise, an INVALID_ARGUMENT error is
            returned.
        ip_address (str):
            The end user's IP address. This field is used to extract
            location information for personalization.

            This field must be either an IPv4 address (e.g.
            "104.133.9.80") or an IPv6 address (e.g.
            "2001:0db8:85a3:0000:0000:8a2e:0370:7334"). Otherwise, an
            INVALID_ARGUMENT error is returned.

            This should not be set when using the JavaScript tag in
            [UserEventService.CollectUserEvent][google.cloud.retail.v2.UserEventService.CollectUserEvent]
            or if
            [direct_user_request][google.cloud.retail.v2.UserInfo.direct_user_request]
            is set.
        user_agent (str):
            User agent as included in the HTTP header.

            The field must be a UTF-8 encoded string with a length limit
            of 1,000 characters. Otherwise, an INVALID_ARGUMENT error is
            returned.

            This should not be set when using the client side event
            reporting with GTM or JavaScript tag in
            [UserEventService.CollectUserEvent][google.cloud.retail.v2.UserEventService.CollectUserEvent]
            or if
            [direct_user_request][google.cloud.retail.v2.UserInfo.direct_user_request]
            is set.
        direct_user_request (bool):
            True if the request is made directly from the end user, in
            which case the
            [ip_address][google.cloud.retail.v2.UserInfo.ip_address] and
            [user_agent][google.cloud.retail.v2.UserInfo.user_agent] can
            be populated from the HTTP request. This flag should be set
            only if the API request is made directly from the end user
            such as a mobile app (and not if a gateway or a server is
            processing and pushing the user events).

            This should not be set when using the JavaScript tag in
            [UserEventService.CollectUserEvent][google.cloud.retail.v2.UserEventService.CollectUserEvent].
    """

    user_id = proto.Field(proto.STRING, number=1,)
    ip_address = proto.Field(proto.STRING, number=2,)
    user_agent = proto.Field(proto.STRING, number=3,)
    direct_user_request = proto.Field(proto.BOOL, number=4,)


__all__ = tuple(sorted(__protobuf__.manifest))
