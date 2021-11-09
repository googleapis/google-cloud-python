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

from google.cloud.retail_v2.types import common
from google.protobuf import duration_pb2  # type: ignore
from google.protobuf import field_mask_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore
from google.protobuf import wrappers_pb2  # type: ignore


__protobuf__ = proto.module(package="google.cloud.retail.v2", manifest={"Product",},)


class Product(proto.Message):
    r"""Product captures all metadata information of items to be
    recommended or searched.

    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        expire_time (google.protobuf.timestamp_pb2.Timestamp):
            The timestamp when this product becomes unavailable for
            [SearchService.Search][google.cloud.retail.v2.SearchService.Search].

            If it is set, the [Product][google.cloud.retail.v2.Product]
            is not available for
            [SearchService.Search][google.cloud.retail.v2.SearchService.Search]
            after
            [expire_time][google.cloud.retail.v2.Product.expire_time].
            However, the product can still be retrieved by
            [ProductService.GetProduct][google.cloud.retail.v2.ProductService.GetProduct]
            and
            [ProductService.ListProducts][google.cloud.retail.v2.ProductService.ListProducts].

            [expire_time][google.cloud.retail.v2.Product.expire_time]
            must be later than
            [available_time][google.cloud.retail.v2.Product.available_time]
            and
            [publish_time][google.cloud.retail.v2.Product.publish_time],
            otherwise an INVALID_ARGUMENT error is thrown.

            Google Merchant Center property
            `expiration_date <https://support.google.com/merchants/answer/6324499>`__.

            This field is a member of `oneof`_ ``expiration``.
        ttl (google.protobuf.duration_pb2.Duration):
            Input only. The TTL (time to live) of the product.

            If it is set, it must be a non-negative value, and
            [expire_time][google.cloud.retail.v2.Product.expire_time] is
            set as current timestamp plus
            [ttl][google.cloud.retail.v2.Product.ttl]. The derived
            [expire_time][google.cloud.retail.v2.Product.expire_time] is
            returned in the output and
            [ttl][google.cloud.retail.v2.Product.ttl] is left blank when
            retrieving the [Product][google.cloud.retail.v2.Product].

            If it is set, the product is not available for
            [SearchService.Search][google.cloud.retail.v2.SearchService.Search]
            after current timestamp plus
            [ttl][google.cloud.retail.v2.Product.ttl]. However, the
            product can still be retrieved by
            [ProductService.GetProduct][google.cloud.retail.v2.ProductService.GetProduct]
            and
            [ProductService.ListProducts][google.cloud.retail.v2.ProductService.ListProducts].

            This field is a member of `oneof`_ ``expiration``.
        name (str):
            Immutable. Full resource name of the product, such as
            ``projects/*/locations/global/catalogs/default_catalog/branches/default_branch/products/product_id``.
        id (str):
            Immutable. [Product][google.cloud.retail.v2.Product]
            identifier, which is the final component of
            [name][google.cloud.retail.v2.Product.name]. For example,
            this field is "id_1", if
            [name][google.cloud.retail.v2.Product.name] is
            ``projects/*/locations/global/catalogs/default_catalog/branches/default_branch/products/id_1``.

            This field must be a UTF-8 encoded string with a length
            limit of 128 characters. Otherwise, an INVALID_ARGUMENT
            error is returned.

            Google Merchant Center property
            `id <https://support.google.com/merchants/answer/6324405>`__.
            Schema.org Property
            `Product.sku <https://schema.org/sku>`__.
        type_ (google.cloud.retail_v2.types.Product.Type):
            Immutable. The type of the product. Default to
            [Catalog.product_level_config.ingestion_product_type][google.cloud.retail.v2.ProductLevelConfig.ingestion_product_type]
            if unset.
        primary_product_id (str):
            Variant group identifier. Must be an
            [id][google.cloud.retail.v2.Product.id], with the same
            parent branch with this product. Otherwise, an error is
            thrown.

            For
            [Type.PRIMARY][google.cloud.retail.v2.Product.Type.PRIMARY]
            [Product][google.cloud.retail.v2.Product]s, this field can
            only be empty or set to the same value as
            [id][google.cloud.retail.v2.Product.id].

            For VARIANT [Product][google.cloud.retail.v2.Product]s, this
            field cannot be empty. A maximum of 2,000 products are
            allowed to share the same
            [Type.PRIMARY][google.cloud.retail.v2.Product.Type.PRIMARY]
            [Product][google.cloud.retail.v2.Product]. Otherwise, an
            INVALID_ARGUMENT error is returned.

            Google Merchant Center Property
            `item_group_id <https://support.google.com/merchants/answer/6324507>`__.
            Schema.org Property
            `Product.inProductGroupWithID <https://schema.org/inProductGroupWithID>`__.

            This field must be enabled before it can be used. `Learn
            more </recommendations-ai/docs/catalog#item-group-id>`__.
        collection_member_ids (Sequence[str]):
            The [id][google.cloud.retail.v2.Product.id] of the
            collection members when
            [type][google.cloud.retail.v2.Product.type] is
            [Type.COLLECTION][google.cloud.retail.v2.Product.Type.COLLECTION].

            Should not set it for other types. A maximum of 1000 values
            are allowed. Otherwise, an INVALID_ARGUMENT error is return.
        gtin (str):
            The Global Trade Item Number (GTIN) of the product.

            This field must be a UTF-8 encoded string with a length
            limit of 128 characters. Otherwise, an INVALID_ARGUMENT
            error is returned.

            This field must be a Unigram. Otherwise, an INVALID_ARGUMENT
            error is returned.

            Google Merchant Center property
            `gtin <https://support.google.com/merchants/answer/6324461>`__.
            Schema.org property
            `Product.isbn <https://schema.org/isbn>`__ or
            `Product.gtin8 <https://schema.org/gtin8>`__ or
            `Product.gtin12 <https://schema.org/gtin12>`__ or
            `Product.gtin13 <https://schema.org/gtin13>`__ or
            `Product.gtin14 <https://schema.org/gtin14>`__.

            If the value is not a valid GTIN, an INVALID_ARGUMENT error
            is returned.
        categories (Sequence[str]):
            Product categories. This field is repeated for supporting
            one product belonging to several parallel categories.
            Strongly recommended using the full path for better search /
            recommendation quality.

            To represent full path of category, use '>' sign to separate
            different hierarchies. If '>' is part of the category name,
            please replace it with other character(s).

            For example, if a shoes product belongs to both ["Shoes &
            Accessories" -> "Shoes"] and ["Sports & Fitness" ->
            "Athletic Clothing" -> "Shoes"], it could be represented as:

            ::

                 "categories": [
                   "Shoes & Accessories > Shoes",
                   "Sports & Fitness > Athletic Clothing > Shoes"
                 ]

            Must be set for
            [Type.PRIMARY][google.cloud.retail.v2.Product.Type.PRIMARY]
            [Product][google.cloud.retail.v2.Product] otherwise an
            INVALID_ARGUMENT error is returned.

            At most 250 values are allowed per
            [Product][google.cloud.retail.v2.Product]. Empty values are
            not allowed. Each value must be a UTF-8 encoded string with
            a length limit of 5,000 characters. Otherwise, an
            INVALID_ARGUMENT error is returned.

            Google Merchant Center property
            `google_product_category <https://support.google.com/merchants/answer/6324436>`__.
            Schema.org property [Product.category]
            (https://schema.org/category).
        title (str):
            Required. Product title.

            This field must be a UTF-8 encoded string with a length
            limit of 1,000 characters. Otherwise, an INVALID_ARGUMENT
            error is returned.

            Google Merchant Center property
            `title <https://support.google.com/merchants/answer/6324415>`__.
            Schema.org property
            `Product.name <https://schema.org/name>`__.
        brands (Sequence[str]):
            The brands of the product.

            A maximum of 30 brands are allowed. Each brand must be a
            UTF-8 encoded string with a length limit of 1,000
            characters. Otherwise, an INVALID_ARGUMENT error is
            returned.

            Google Merchant Center property
            `brand <https://support.google.com/merchants/answer/6324351>`__.
            Schema.org property
            `Product.brand <https://schema.org/brand>`__.
        description (str):
            Product description.

            This field must be a UTF-8 encoded string with a length
            limit of 5,000 characters. Otherwise, an INVALID_ARGUMENT
            error is returned.

            Google Merchant Center property
            `description <https://support.google.com/merchants/answer/6324468>`__.
            schema.org property
            `Product.description <https://schema.org/description>`__.
        language_code (str):
            Language of the title/description and other string
            attributes. Use language tags defined by [BCP
            47][https://www.rfc-editor.org/rfc/bcp/bcp47.txt].

            For product prediction, this field is ignored and the model
            automatically detects the text language. The
            [Product][google.cloud.retail.v2.Product] can include text
            in different languages, but duplicating
            [Product][google.cloud.retail.v2.Product]s to provide text
            in multiple languages can result in degraded model
            performance.

            For product search this field is in use. It defaults to
            "en-US" if unset.
        attributes (Sequence[google.cloud.retail_v2.types.Product.AttributesEntry]):
            Highly encouraged. Extra product attributes to be included.
            For example, for products, this could include the store
            name, vendor, style, color, etc. These are very strong
            signals for recommendation model, thus we highly recommend
            providing the attributes here.

            Features that can take on one of a limited number of
            possible values. Two types of features can be set are:

            Textual features. some examples would be the brand/maker of
            a product, or country of a customer. Numerical features.
            Some examples would be the height/weight of a product, or
            age of a customer.

            For example:
            ``{ "vendor": {"text": ["vendor123", "vendor456"]}, "lengths_cm": {"numbers":[2.3, 15.4]}, "heights_cm": {"numbers":[8.1, 6.4]} }``.

            This field needs to pass all below criteria, otherwise an
            INVALID_ARGUMENT error is returned:

            -  Max entries count: 200.
            -  The key must be a UTF-8 encoded string with a length
               limit of 128 characters.
            -  For indexable attribute, the key must match the pattern:
               ``[a-zA-Z0-9][a-zA-Z0-9_]*``. For example, key0LikeThis
               or KEY_1_LIKE_THIS.
        tags (Sequence[str]):
            Custom tags associated with the product.

            At most 250 values are allowed per
            [Product][google.cloud.retail.v2.Product]. This value must
            be a UTF-8 encoded string with a length limit of 1,000
            characters. Otherwise, an INVALID_ARGUMENT error is
            returned.

            This tag can be used for filtering recommendation results by
            passing the tag as part of the
            [PredictRequest.filter][google.cloud.retail.v2.PredictRequest.filter].

            Google Merchant Center property
            `custom_label_0–4 <https://support.google.com/merchants/answer/6324473>`__.
        price_info (google.cloud.retail_v2.types.PriceInfo):
            Product price and cost information.

            Google Merchant Center property
            `price <https://support.google.com/merchants/answer/6324371>`__.
        rating (google.cloud.retail_v2.types.Rating):
            The rating of this product.
        available_time (google.protobuf.timestamp_pb2.Timestamp):
            The timestamp when this
            [Product][google.cloud.retail.v2.Product] becomes available
            for
            [SearchService.Search][google.cloud.retail.v2.SearchService.Search].
        availability (google.cloud.retail_v2.types.Product.Availability):
            The online availability of the
            [Product][google.cloud.retail.v2.Product]. Default to
            [Availability.IN_STOCK][google.cloud.retail.v2.Product.Availability.IN_STOCK].

            Google Merchant Center Property
            `availability <https://support.google.com/merchants/answer/6324448>`__.
            Schema.org Property
            `Offer.availability <https://schema.org/availability>`__.
        available_quantity (google.protobuf.wrappers_pb2.Int32Value):
            The available quantity of the item.
        fulfillment_info (Sequence[google.cloud.retail_v2.types.FulfillmentInfo]):
            Fulfillment information, such as the store IDs for in-store
            pickup or region IDs for different shipping methods.

            All the elements must have distinct
            [FulfillmentInfo.type][google.cloud.retail.v2.FulfillmentInfo.type].
            Otherwise, an INVALID_ARGUMENT error is returned.
        uri (str):
            Canonical URL directly linking to the product detail page.

            It is strongly recommended to provide a valid uri for the
            product, otherwise the service performance could be
            significantly degraded.

            This field must be a UTF-8 encoded string with a length
            limit of 5,000 characters. Otherwise, an INVALID_ARGUMENT
            error is returned.

            Google Merchant Center property
            `link <https://support.google.com/merchants/answer/6324416>`__.
            Schema.org property `Offer.url <https://schema.org/url>`__.
        images (Sequence[google.cloud.retail_v2.types.Image]):
            Product images for the product.Highly recommended to put the
            main image to the first.

            A maximum of 300 images are allowed.

            Google Merchant Center property
            `image_link <https://support.google.com/merchants/answer/6324350>`__.
            Schema.org property
            `Product.image <https://schema.org/image>`__.
        audience (google.cloud.retail_v2.types.Audience):
            The target group associated with a given
            audience (e.g. male, veterans, car owners,
            musicians, etc.) of the product.
        color_info (google.cloud.retail_v2.types.ColorInfo):
            The color of the product.

            Google Merchant Center property
            `color <https://support.google.com/merchants/answer/6324487>`__.
            Schema.org property
            `Product.color <https://schema.org/color>`__.
        sizes (Sequence[str]):
            The size of the product. To represent different size systems
            or size types, consider using this format:
            [[[size_system:]size_type:]size_value].

            For example, in "US:MENS:M", "US" represents size system;
            "MENS" represents size type; "M" represents size value. In
            "GIRLS:27", size system is empty; "GIRLS" represents size
            type; "27" represents size value. In "32 inches", both size
            system and size type are empty, while size value is "32
            inches".

            A maximum of 20 values are allowed per
            [Product][google.cloud.retail.v2.Product]. Each value must
            be a UTF-8 encoded string with a length limit of 128
            characters. Otherwise, an INVALID_ARGUMENT error is
            returned.

            Google Merchant Center property
            `size <https://support.google.com/merchants/answer/6324492>`__,
            `size_type <https://support.google.com/merchants/answer/6324497>`__
            and
            `size_system <https://support.google.com/merchants/answer/6324502>`__.
            Schema.org property
            `Product.size <https://schema.org/size>`__.
        materials (Sequence[str]):
            The material of the product. For example, "leather",
            "wooden".

            A maximum of 20 values are allowed. Each value must be a
            UTF-8 encoded string with a length limit of 128 characters.
            Otherwise, an INVALID_ARGUMENT error is returned.

            Google Merchant Center property
            `material <https://support.google.com/merchants/answer/6324410>`__.
            Schema.org property
            `Product.material <https://schema.org/material>`__.
        patterns (Sequence[str]):
            The pattern or graphic print of the product. For example,
            "striped", "polka dot", "paisley".

            A maximum of 20 values are allowed per
            [Product][google.cloud.retail.v2.Product]. Each value must
            be a UTF-8 encoded string with a length limit of 128
            characters. Otherwise, an INVALID_ARGUMENT error is
            returned.

            Google Merchant Center property
            `pattern <https://support.google.com/merchants/answer/6324483>`__.
            Schema.org property
            `Product.pattern <https://schema.org/pattern>`__.
        conditions (Sequence[str]):
            The condition of the product. Strongly encouraged to use the
            standard values: "new", "refurbished", "used".

            A maximum of 5 values are allowed per
            [Product][google.cloud.retail.v2.Product]. Each value must
            be a UTF-8 encoded string with a length limit of 128
            characters. Otherwise, an INVALID_ARGUMENT error is
            returned.

            Google Merchant Center property
            `condition <https://support.google.com/merchants/answer/6324469>`__.
            Schema.org property
            `Offer.itemCondition <https://schema.org/itemCondition>`__.
        promotions (Sequence[google.cloud.retail_v2.types.Promotion]):
            The promotions applied to the product. A maximum of 10
            values are allowed per
            [Product][google.cloud.retail.v2.Product].
        publish_time (google.protobuf.timestamp_pb2.Timestamp):
            The timestamp when the product is published by the retailer
            for the first time, which indicates the freshness of the
            products. Note that this field is different from
            [available_time][google.cloud.retail.v2.Product.available_time],
            given it purely describes product freshness regardless of
            when it is available on search and recommendation.
        retrievable_fields (google.protobuf.field_mask_pb2.FieldMask):
            Indicates which fields in the
            [Product][google.cloud.retail.v2.Product]s are returned in
            [SearchResponse][google.cloud.retail.v2.SearchResponse].

            Supported fields for all
            [type][google.cloud.retail.v2.Product.type]s:

            -  [audience][google.cloud.retail.v2.Product.audience]
            -  [availability][google.cloud.retail.v2.Product.availability]
            -  [brands][google.cloud.retail.v2.Product.brands]
            -  [color_info][google.cloud.retail.v2.Product.color_info]
            -  [conditions][google.cloud.retail.v2.Product.conditions]
            -  [gtin][google.cloud.retail.v2.Product.gtin]
            -  [materials][google.cloud.retail.v2.Product.materials]
            -  [name][google.cloud.retail.v2.Product.name]
            -  [patterns][google.cloud.retail.v2.Product.patterns]
            -  [price_info][google.cloud.retail.v2.Product.price_info]
            -  [rating][google.cloud.retail.v2.Product.rating]
            -  [sizes][google.cloud.retail.v2.Product.sizes]
            -  [title][google.cloud.retail.v2.Product.title]
            -  [uri][google.cloud.retail.v2.Product.uri]

            Supported fields only for
            [Type.PRIMARY][google.cloud.retail.v2.Product.Type.PRIMARY]
            and
            [Type.COLLECTION][google.cloud.retail.v2.Product.Type.COLLECTION]:

            -  [categories][google.cloud.retail.v2.Product.categories]
            -  [description][google.cloud.retail.v2.Product.description]
            -  [images][google.cloud.retail.v2.Product.images]

            Supported fields only for
            [Type.VARIANT][google.cloud.retail.v2.Product.Type.VARIANT]:

            -  Only the first image in
               [images][google.cloud.retail.v2.Product.images]

            To mark
            [attributes][google.cloud.retail.v2.Product.attributes] as
            retrievable, include paths of the form "attributes.key"
            where "key" is the key of a custom attribute, as specified
            in [attributes][google.cloud.retail.v2.Product.attributes].

            For
            [Type.PRIMARY][google.cloud.retail.v2.Product.Type.PRIMARY]
            and
            [Type.COLLECTION][google.cloud.retail.v2.Product.Type.COLLECTION],
            the following fields are always returned in
            [SearchResponse][google.cloud.retail.v2.SearchResponse] by
            default:

            -  [name][google.cloud.retail.v2.Product.name]

            For
            [Type.VARIANT][google.cloud.retail.v2.Product.Type.VARIANT],
            the following fields are always returned in by default:

            -  [name][google.cloud.retail.v2.Product.name]
            -  [color_info][google.cloud.retail.v2.Product.color_info]

            Maximum number of paths is 30. Otherwise, an
            INVALID_ARGUMENT error is returned.

            Note: Returning more fields in
            [SearchResponse][google.cloud.retail.v2.SearchResponse] may
            increase response payload size and serving latency.
        variants (Sequence[google.cloud.retail_v2.types.Product]):
            Output only. Product variants grouped together on primary
            product which share similar product attributes. It's
            automatically grouped by
            [primary_product_id][google.cloud.retail.v2.Product.primary_product_id]
            for all the product variants. Only populated for
            [Type.PRIMARY][google.cloud.retail.v2.Product.Type.PRIMARY]
            [Product][google.cloud.retail.v2.Product]s.

            Note: This field is OUTPUT_ONLY for
            [ProductService.GetProduct][google.cloud.retail.v2.ProductService.GetProduct].
            Do not set this field in API requests.
    """

    class Type(proto.Enum):
        r"""The type of this product."""
        TYPE_UNSPECIFIED = 0
        PRIMARY = 1
        VARIANT = 2
        COLLECTION = 3

    class Availability(proto.Enum):
        r"""Product availability. If this field is unspecified, the
        product is assumed to be in stock.
        """
        AVAILABILITY_UNSPECIFIED = 0
        IN_STOCK = 1
        OUT_OF_STOCK = 2
        PREORDER = 3
        BACKORDER = 4

    expire_time = proto.Field(
        proto.MESSAGE, number=16, oneof="expiration", message=timestamp_pb2.Timestamp,
    )
    ttl = proto.Field(
        proto.MESSAGE, number=17, oneof="expiration", message=duration_pb2.Duration,
    )
    name = proto.Field(proto.STRING, number=1,)
    id = proto.Field(proto.STRING, number=2,)
    type_ = proto.Field(proto.ENUM, number=3, enum=Type,)
    primary_product_id = proto.Field(proto.STRING, number=4,)
    collection_member_ids = proto.RepeatedField(proto.STRING, number=5,)
    gtin = proto.Field(proto.STRING, number=6,)
    categories = proto.RepeatedField(proto.STRING, number=7,)
    title = proto.Field(proto.STRING, number=8,)
    brands = proto.RepeatedField(proto.STRING, number=9,)
    description = proto.Field(proto.STRING, number=10,)
    language_code = proto.Field(proto.STRING, number=11,)
    attributes = proto.MapField(
        proto.STRING, proto.MESSAGE, number=12, message=common.CustomAttribute,
    )
    tags = proto.RepeatedField(proto.STRING, number=13,)
    price_info = proto.Field(proto.MESSAGE, number=14, message=common.PriceInfo,)
    rating = proto.Field(proto.MESSAGE, number=15, message=common.Rating,)
    available_time = proto.Field(
        proto.MESSAGE, number=18, message=timestamp_pb2.Timestamp,
    )
    availability = proto.Field(proto.ENUM, number=19, enum=Availability,)
    available_quantity = proto.Field(
        proto.MESSAGE, number=20, message=wrappers_pb2.Int32Value,
    )
    fulfillment_info = proto.RepeatedField(
        proto.MESSAGE, number=21, message=common.FulfillmentInfo,
    )
    uri = proto.Field(proto.STRING, number=22,)
    images = proto.RepeatedField(proto.MESSAGE, number=23, message=common.Image,)
    audience = proto.Field(proto.MESSAGE, number=24, message=common.Audience,)
    color_info = proto.Field(proto.MESSAGE, number=25, message=common.ColorInfo,)
    sizes = proto.RepeatedField(proto.STRING, number=26,)
    materials = proto.RepeatedField(proto.STRING, number=27,)
    patterns = proto.RepeatedField(proto.STRING, number=28,)
    conditions = proto.RepeatedField(proto.STRING, number=29,)
    promotions = proto.RepeatedField(
        proto.MESSAGE, number=34, message=common.Promotion,
    )
    publish_time = proto.Field(
        proto.MESSAGE, number=33, message=timestamp_pb2.Timestamp,
    )
    retrievable_fields = proto.Field(
        proto.MESSAGE, number=30, message=field_mask_pb2.FieldMask,
    )
    variants = proto.RepeatedField(proto.MESSAGE, number=31, message="Product",)


__all__ = tuple(sorted(__protobuf__.manifest))
