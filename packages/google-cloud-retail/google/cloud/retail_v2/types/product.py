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
from google.protobuf import timestamp_pb2  # type: ignore
from google.protobuf import wrappers_pb2  # type: ignore


__protobuf__ = proto.module(package="google.cloud.retail.v2", manifest={"Product",},)


class Product(proto.Message):
    r"""Product captures all metadata information of items to be
    recommended or searched.

    Attributes:
        name (str):
            Immutable. Full resource name of the product, such as
            ``projects/*/locations/global/catalogs/default_catalog/branches/default_branch/products/product_id``.

            The branch ID must be "default_branch".
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
            Immutable. The type of the product. This
            field is output-only.
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
            limit of 128 characters. Otherwise, an INVALID_ARGUMENT
            error is returned.

            Google Merchant Center property
            `title <https://support.google.com/merchants/answer/6324415>`__.
            Schema.org property
            `Product.name <https://schema.org/name>`__.
        description (str):
            Product description.

            This field must be a UTF-8 encoded string with a length
            limit of 5,000 characters. Otherwise, an INVALID_ARGUMENT
            error is returned.

            Google Merchant Center property
            `description <https://support.google.com/merchants/answer/6324468>`__.
            schema.org property
            `Product.description <https://schema.org/description>`__.
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

            A maximum of 150 attributes are allowed. Otherwise, an
            INVALID_ARGUMENT error is returned.

            The key must be a UTF-8 encoded string with a length limit
            of 5,000 characters. Otherwise, an INVALID_ARGUMENT error is
            returned.
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
        available_time (google.protobuf.timestamp_pb2.Timestamp):
            The timestamp when this
            [Product][google.cloud.retail.v2.Product] becomes available
            recommendation and search.
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
        uri (str):
            Canonical URL directly linking to the product detail page.

            This field must be a UTF-8 encoded string with a length
            limit of 5,000 characters. Otherwise, an INVALID_ARGUMENT
            error is returned.

            Google Merchant Center property
            `link <https://support.google.com/merchants/answer/6324416>`__.
            Schema.org property `Offer.url <https://schema.org/url>`__.
        images (Sequence[google.cloud.retail_v2.types.Image]):
            Product images for the product.

            A maximum of 300 images are allowed.

            Google Merchant Center property
            `image_link <https://support.google.com/merchants/answer/6324350>`__.
            Schema.org property
            `Product.image <https://schema.org/image>`__.
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

    name = proto.Field(proto.STRING, number=1,)
    id = proto.Field(proto.STRING, number=2,)
    type_ = proto.Field(proto.ENUM, number=3, enum=Type,)
    primary_product_id = proto.Field(proto.STRING, number=4,)
    categories = proto.RepeatedField(proto.STRING, number=7,)
    title = proto.Field(proto.STRING, number=8,)
    description = proto.Field(proto.STRING, number=10,)
    attributes = proto.MapField(
        proto.STRING, proto.MESSAGE, number=12, message=common.CustomAttribute,
    )
    tags = proto.RepeatedField(proto.STRING, number=13,)
    price_info = proto.Field(proto.MESSAGE, number=14, message=common.PriceInfo,)
    available_time = proto.Field(
        proto.MESSAGE, number=18, message=timestamp_pb2.Timestamp,
    )
    availability = proto.Field(proto.ENUM, number=19, enum=Availability,)
    available_quantity = proto.Field(
        proto.MESSAGE, number=20, message=wrappers_pb2.Int32Value,
    )
    uri = proto.Field(proto.STRING, number=22,)
    images = proto.RepeatedField(proto.MESSAGE, number=23, message=common.Image,)


__all__ = tuple(sorted(__protobuf__.manifest))
