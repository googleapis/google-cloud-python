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

from google.protobuf import timestamp_pb2  # type: ignore


__protobuf__ = proto.module(
    package="google.cloud.retail.v2",
    manifest={
        "Audience",
        "ColorInfo",
        "CustomAttribute",
        "FulfillmentInfo",
        "Image",
        "Interval",
        "PriceInfo",
        "Rating",
        "UserInfo",
        "Promotion",
    },
)


class Audience(proto.Message):
    r"""An intended audience of the
    [Product][google.cloud.retail.v2.Product] for whom it's sold.

    Attributes:
        genders (Sequence[str]):
            The genders of the audience. Strongly encouraged to use the
            standard values: "male", "female", "unisex".

            At most 5 values are allowed. Each value must be a UTF-8
            encoded string with a length limit of 128 characters.
            Otherwise, an INVALID_ARGUMENT error is returned.

            Google Merchant Center property
            `gender <https://support.google.com/merchants/answer/6324479>`__.
            Schema.org property
            `Product.audience.suggestedGender <https://schema.org/suggestedGender>`__.
        age_groups (Sequence[str]):
            The age groups of the audience. Strongly encouraged to use
            the standard values: "newborn" (up to 3 months old),
            "infant" (3–12 months old), "toddler" (1–5 years old),
            "kids" (5–13 years old), "adult" (typically teens or older).

            At most 5 values are allowed. Each value must be a UTF-8
            encoded string with a length limit of 128 characters.
            Otherwise, an INVALID_ARGUMENT error is returned.

            Google Merchant Center property
            `age_group <https://support.google.com/merchants/answer/6324463>`__.
            Schema.org property
            `Product.audience.suggestedMinAge <https://schema.org/suggestedMinAge>`__
            and
            `Product.audience.suggestedMaxAge <https://schema.org/suggestedMaxAge>`__.
    """

    genders = proto.RepeatedField(proto.STRING, number=1,)
    age_groups = proto.RepeatedField(proto.STRING, number=2,)


class ColorInfo(proto.Message):
    r"""The color information of a
    [Product][google.cloud.retail.v2.Product].

    Attributes:
        color_families (Sequence[str]):
            The standard color families. Strongly recommended to use the
            following standard color groups: "Red", "Pink", "Orange",
            "Yellow", "Purple", "Green", "Cyan", "Blue", "Brown",
            "White", "Gray", "Black" and "Mixed". Normally it is
            expected to have only 1 color family. May consider using
            single "Mixed" instead of multiple values.

            A maximum of 5 values are allowed. Each value must be a
            UTF-8 encoded string with a length limit of 128 characters.
            Otherwise, an INVALID_ARGUMENT error is returned.

            Google Merchant Center property
            `color <https://support.google.com/merchants/answer/6324487>`__.
            Schema.org property
            `Product.color <https://schema.org/color>`__.
        colors (Sequence[str]):
            The color display names, which may be different from
            standard color family names, such as the color aliases used
            in the website frontend. Normally it is expected to have
            only 1 color. May consider using single "Mixed" instead of
            multiple values.

            A maximum of 5 colors are allowed. Each value must be a
            UTF-8 encoded string with a length limit of 128 characters.
            Otherwise, an INVALID_ARGUMENT error is returned.

            Google Merchant Center property
            `color <https://support.google.com/merchants/answer/6324487>`__.
            Schema.org property
            `Product.color <https://schema.org/color>`__.
    """

    color_families = proto.RepeatedField(proto.STRING, number=1,)
    colors = proto.RepeatedField(proto.STRING, number=2,)


class CustomAttribute(proto.Message):
    r"""A custom attribute that is not explicitly modeled in
    [Product][google.cloud.retail.v2.Product].

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
        searchable (bool):
            If true, custom attribute values are searchable by text
            queries in
            [SearchService.Search][google.cloud.retail.v2.SearchService.Search].

            This field is ignored in a
            [UserEvent][google.cloud.retail.v2.UserEvent].

            Only set if type
            [text][google.cloud.retail.v2.CustomAttribute.text] is set.
            Otherwise, a INVALID_ARGUMENT error is returned.
        indexable (bool):
            If true, custom attribute values are indexed, so that it can
            be filtered, faceted or boosted in
            [SearchService.Search][google.cloud.retail.v2.SearchService.Search].

            This field is ignored in a
            [UserEvent][google.cloud.retail.v2.UserEvent].

            See
            [SearchRequest.filter][google.cloud.retail.v2.SearchRequest.filter],
            [SearchRequest.facet_specs][google.cloud.retail.v2.SearchRequest.facet_specs]
            and
            [SearchRequest.boost_spec][google.cloud.retail.v2.SearchRequest.boost_spec]
            for more details.
    """

    text = proto.RepeatedField(proto.STRING, number=1,)
    numbers = proto.RepeatedField(proto.DOUBLE, number=2,)
    searchable = proto.Field(proto.BOOL, number=3, optional=True,)
    indexable = proto.Field(proto.BOOL, number=4, optional=True,)


class FulfillmentInfo(proto.Message):
    r"""Fulfillment information, such as the store IDs for in-store
    pickup or region IDs for different shipping methods.

    Attributes:
        type_ (str):
            The fulfillment type, including commonly used types (such as
            pickup in store and same day delivery), and custom types.
            Customers have to map custom types to their display names
            before rendering UI.

            Supported values:

            -  "pickup-in-store"
            -  "ship-to-store"
            -  "same-day-delivery"
            -  "next-day-delivery"
            -  "custom-type-1"
            -  "custom-type-2"
            -  "custom-type-3"
            -  "custom-type-4"
            -  "custom-type-5"

            If this field is set to an invalid value other than these,
            an INVALID_ARGUMENT error is returned.
        place_ids (Sequence[str]):
            The IDs for this
            [type][google.cloud.retail.v2.FulfillmentInfo.type], such as
            the store IDs for
            [FulfillmentInfo.type.pickup-in-store][google.cloud.retail.v2.FulfillmentInfo.type]
            or the region IDs for
            [FulfillmentInfo.type.same-day-delivery][google.cloud.retail.v2.FulfillmentInfo.type].

            A maximum of 2000 values are allowed. Each value must be a
            string with a length limit of 10 characters, matching the
            pattern [a-zA-Z0-9\_-]+, such as "store1" or "REGION-2".
            Otherwise, an INVALID_ARGUMENT error is returned.
    """

    type_ = proto.Field(proto.STRING, number=1,)
    place_ids = proto.RepeatedField(proto.STRING, number=2,)


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


class Interval(proto.Message):
    r"""A floating point interval.
    Attributes:
        minimum (float):
            Inclusive lower bound.
        exclusive_minimum (float):
            Exclusive lower bound.
        maximum (float):
            Inclusive upper bound.
        exclusive_maximum (float):
            Exclusive upper bound.
    """

    minimum = proto.Field(proto.DOUBLE, number=1, oneof="min",)
    exclusive_minimum = proto.Field(proto.DOUBLE, number=2, oneof="min",)
    maximum = proto.Field(proto.DOUBLE, number=3, oneof="max",)
    exclusive_maximum = proto.Field(proto.DOUBLE, number=4, oneof="max",)


class PriceInfo(proto.Message):
    r"""The price information of a
    [Product][google.cloud.retail.v2.Product].

    Attributes:
        currency_code (str):
            The 3-letter currency code defined in `ISO
            4217 <https://www.iso.org/iso-4217-currency-codes.html>`__.

            If this field is an unrecognizable currency code, an
            INVALID_ARGUMENT error is returned.

            The
            [Product.Type.VARIANT][google.cloud.retail.v2.Product.Type.VARIANT]
            [Product][google.cloud.retail.v2.Product]s with the same
            [Product.primary_product_id][google.cloud.retail.v2.Product.primary_product_id]
            must share the same
            [currency_code][google.cloud.retail.v2.PriceInfo.currency_code].
            Otherwise, a FAILED_PRECONDITION error is returned.
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
        price_effective_time (google.protobuf.timestamp_pb2.Timestamp):
            The timestamp when the
            [price][google.cloud.retail.v2.PriceInfo.price] starts to be
            effective. This can be set as a future timestamp, and the
            [price][google.cloud.retail.v2.PriceInfo.price] is only used
            for search after
            [price_effective_time][google.cloud.retail.v2.PriceInfo.price_effective_time].
            If so, the
            [original_price][google.cloud.retail.v2.PriceInfo.original_price]
            must be set and
            [original_price][google.cloud.retail.v2.PriceInfo.original_price]
            is used before
            [price_effective_time][google.cloud.retail.v2.PriceInfo.price_effective_time].

            Do not set if
            [price][google.cloud.retail.v2.PriceInfo.price] is always
            effective because it will cause additional latency during
            search.
        price_expire_time (google.protobuf.timestamp_pb2.Timestamp):
            The timestamp when the
            [price][google.cloud.retail.v2.PriceInfo.price] stops to be
            effective. The
            [price][google.cloud.retail.v2.PriceInfo.price] is used for
            search before
            [price_expire_time][google.cloud.retail.v2.PriceInfo.price_expire_time].
            If this field is set, the
            [original_price][google.cloud.retail.v2.PriceInfo.original_price]
            must be set and
            [original_price][google.cloud.retail.v2.PriceInfo.original_price]
            is used after
            [price_expire_time][google.cloud.retail.v2.PriceInfo.price_expire_time].

            Do not set if
            [price][google.cloud.retail.v2.PriceInfo.price] is always
            effective because it will cause additional latency during
            search.
        price_range (google.cloud.retail_v2.types.PriceInfo.PriceRange):
            Output only. The price range of all the child
            [Product.Type.VARIANT][google.cloud.retail.v2.Product.Type.VARIANT]
            [Product][google.cloud.retail.v2.Product]s grouped together
            on the
            [Product.Type.PRIMARY][google.cloud.retail.v2.Product.Type.PRIMARY]
            [Product][google.cloud.retail.v2.Product]. Only populated
            for
            [Product.Type.PRIMARY][google.cloud.retail.v2.Product.Type.PRIMARY]
            [Product][google.cloud.retail.v2.Product]s.

            Note: This field is OUTPUT_ONLY for
            [ProductService.GetProduct][google.cloud.retail.v2.ProductService.GetProduct].
            Do not set this field in API requests.
    """

    class PriceRange(proto.Message):
        r"""The price range of all
        [variant][google.cloud.retail.v2.Product.Type.VARIANT]
        [Product][google.cloud.retail.v2.Product] having the same
        [Product.primary_product_id][google.cloud.retail.v2.Product.primary_product_id].

        Attributes:
            price (google.cloud.retail_v2.types.Interval):
                The inclusive
                [Product.pricing_info.price][google.cloud.retail.v2.PriceInfo.price]
                interval of all
                [variant][google.cloud.retail.v2.Product.Type.VARIANT]
                [Product][google.cloud.retail.v2.Product] having the same
                [Product.primary_product_id][google.cloud.retail.v2.Product.primary_product_id].
            original_price (google.cloud.retail_v2.types.Interval):
                The inclusive
                [Product.pricing_info.original_price][google.cloud.retail.v2.PriceInfo.original_price]
                internal of all
                [variant][google.cloud.retail.v2.Product.Type.VARIANT]
                [Product][google.cloud.retail.v2.Product] having the same
                [Product.primary_product_id][google.cloud.retail.v2.Product.primary_product_id].
        """

        price = proto.Field(proto.MESSAGE, number=1, message="Interval",)
        original_price = proto.Field(proto.MESSAGE, number=2, message="Interval",)

    currency_code = proto.Field(proto.STRING, number=1,)
    price = proto.Field(proto.FLOAT, number=2,)
    original_price = proto.Field(proto.FLOAT, number=3,)
    cost = proto.Field(proto.FLOAT, number=4,)
    price_effective_time = proto.Field(
        proto.MESSAGE, number=5, message=timestamp_pb2.Timestamp,
    )
    price_expire_time = proto.Field(
        proto.MESSAGE, number=6, message=timestamp_pb2.Timestamp,
    )
    price_range = proto.Field(proto.MESSAGE, number=7, message=PriceRange,)


class Rating(proto.Message):
    r"""The rating of a [Product][google.cloud.retail.v2.Product].
    Attributes:
        rating_count (int):
            The total number of ratings. This value is independent of
            the value of
            [rating_histogram][google.cloud.retail.v2.Rating.rating_histogram].

            This value must be nonnegative. Otherwise, an
            INVALID_ARGUMENT error is returned.
        average_rating (float):
            The average rating of the
            [Product][google.cloud.retail.v2.Product].

            The rating is scaled at 1-5. Otherwise, an INVALID_ARGUMENT
            error is returned.
        rating_histogram (Sequence[int]):
            List of rating counts per rating value (index = rating - 1).
            The list is empty if there is no rating. If the list is
            non-empty, its size is always 5. Otherwise, an
            INVALID_ARGUMENT error is returned.

            For example, [41, 14, 13, 47, 303]. It means that the
            [Product][google.cloud.retail.v2.Product] got 41 ratings
            with 1 star, 14 ratings with 2 star, and so on.
    """

    rating_count = proto.Field(proto.INT32, number=1,)
    average_rating = proto.Field(proto.FLOAT, number=2,)
    rating_histogram = proto.RepeatedField(proto.INT32, number=3,)


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
            The end user's IP address. Required for getting
            [SearchResponse.sponsored_results][google.cloud.retail.v2.SearchResponse.sponsored_results].
            This field is used to extract location information for
            personalization.

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
            User agent as included in the HTTP header. Required for
            getting
            [SearchResponse.sponsored_results][google.cloud.retail.v2.SearchResponse.sponsored_results].

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


class Promotion(proto.Message):
    r"""Promotion information.
    Attributes:
        promotion_id (str):
            ID of the promotion. For example, "free gift".

            The value value must be a UTF-8 encoded string with a length
            limit of 128 characters, and match the pattern:
            [a-zA-Z][a-zA-Z0-9\_]*. For example, id0LikeThis or
            ID_1_LIKE_THIS. Otherwise, an INVALID_ARGUMENT error is
            returned.

            Google Merchant Center property
            `promotion <https://support.google.com/merchants/answer/7050148>`__.
    """

    promotion_id = proto.Field(proto.STRING, number=1,)


__all__ = tuple(sorted(__protobuf__.manifest))
