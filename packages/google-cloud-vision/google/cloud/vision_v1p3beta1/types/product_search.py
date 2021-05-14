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

from google.cloud.vision_v1p3beta1.types import geometry
from google.cloud.vision_v1p3beta1.types import product_search_service
from google.protobuf import timestamp_pb2  # type: ignore


__protobuf__ = proto.module(
    package="google.cloud.vision.v1p3beta1",
    manifest={
        "ProductSearchCategory",
        "ProductSearchResultsView",
        "ProductSearchParams",
        "ProductSearchResults",
    },
)


class ProductSearchCategory(proto.Enum):
    r"""Supported product search categories."""
    PRODUCT_SEARCH_CATEGORY_UNSPECIFIED = 0
    SHOES = 1
    BAGS = 2


class ProductSearchResultsView(proto.Enum):
    r"""Specifies the fields to include in product search results."""
    BASIC = 0
    FULL = 1


class ProductSearchParams(proto.Message):
    r"""Parameters for a product search request.
    Attributes:
        catalog_name (str):
            The resource name of the catalog to search.

            Format is: ``productSearch/catalogs/CATALOG_NAME``.
        category (google.cloud.vision_v1p3beta1.types.ProductSearchCategory):
            The category to search in. Optional. It is inferred by the
            system if it is not specified. [Deprecated] Use
            ``product_category``.
        product_category (str):
            The product category to search in. Optional. It is inferred
            by the system if it is not specified. Supported values are
            ``bag``, ``shoe``, ``sunglasses``, ``dress``, ``outerwear``,
            ``skirt``, ``top``, ``shorts``, and ``pants``.
        normalized_bounding_poly (google.cloud.vision_v1p3beta1.types.NormalizedBoundingPoly):
            The bounding polygon around the area of interest in the
            image. Optional. If it is not specified, system discretion
            will be applied. [Deprecated] Use ``bounding_poly``.
        bounding_poly (google.cloud.vision_v1p3beta1.types.BoundingPoly):
            The bounding polygon around the area of
            interest in the image. Optional. If it is not
            specified, system discretion will be applied.
        view (google.cloud.vision_v1p3beta1.types.ProductSearchResultsView):
            Specifies the verbosity of the product search results.
            Optional. Defaults to ``BASIC``.
        product_set (str):
            The resource name of a
            [ProductSet][google.cloud.vision.v1p3beta1.ProductSet] to be
            searched for similar images.

            Format is:
            ``projects/PROJECT_ID/locations/LOC_ID/productSets/PRODUCT_SET_ID``.
        product_categories (Sequence[str]):
            The list of product categories to search in.
            Currently, we only consider the first category,
            and either "homegoods" or "apparel" should be
            specified.
        filter (str):
            The filtering expression. This can be used to
            restrict search results based on Product labels.
            We currently support an AND of OR of key-value
            expressions, where each expression within an OR
            must have the same key.
            For example, "(color = red OR color = blue) AND
            brand = Google" is acceptable, but not "(color =
            red OR brand = Google)" or "color: red".
    """

    catalog_name = proto.Field(proto.STRING, number=1,)
    category = proto.Field(proto.ENUM, number=2, enum="ProductSearchCategory",)
    product_category = proto.Field(proto.STRING, number=5,)
    normalized_bounding_poly = proto.Field(
        proto.MESSAGE, number=3, message=geometry.NormalizedBoundingPoly,
    )
    bounding_poly = proto.Field(proto.MESSAGE, number=9, message=geometry.BoundingPoly,)
    view = proto.Field(proto.ENUM, number=4, enum="ProductSearchResultsView",)
    product_set = proto.Field(proto.STRING, number=6,)
    product_categories = proto.RepeatedField(proto.STRING, number=7,)
    filter = proto.Field(proto.STRING, number=8,)


class ProductSearchResults(proto.Message):
    r"""Results for a product search request.
    Attributes:
        category (google.cloud.vision_v1p3beta1.types.ProductSearchCategory):
            Product category. [Deprecated] Use ``product_category``.
        product_category (str):
            Product category. Supported values are ``bag`` and ``shoe``.
            [Deprecated] ``product_category`` is provided in each
            Product.
        index_time (google.protobuf.timestamp_pb2.Timestamp):
            Timestamp of the index which provided these
            results. Changes made after this time are not
            reflected in the current results.
        products (Sequence[google.cloud.vision_v1p3beta1.types.ProductSearchResults.ProductInfo]):
            List of detected products.
        results (Sequence[google.cloud.vision_v1p3beta1.types.ProductSearchResults.Result]):
            List of results, one for each product match.
    """

    class ProductInfo(proto.Message):
        r"""Information about a product.
        Attributes:
            product_id (str):
                Product ID.
            image_uri (str):
                The URI of the image which matched the query image.

                This field is returned only if ``view`` is set to ``FULL``
                in the request.
            score (float):
                A confidence level on the match, ranging from 0 (no
                confidence) to 1 (full confidence).

                This field is returned only if ``view`` is set to ``FULL``
                in the request.
        """

        product_id = proto.Field(proto.STRING, number=1,)
        image_uri = proto.Field(proto.STRING, number=2,)
        score = proto.Field(proto.FLOAT, number=3,)

    class Result(proto.Message):
        r"""Information about a product.
        Attributes:
            product (google.cloud.vision_v1p3beta1.types.Product):
                The Product.
            score (float):
                A confidence level on the match, ranging from 0 (no
                confidence) to 1 (full confidence).

                This field is returned only if ``view`` is set to ``FULL``
                in the request.
            image (str):
                The resource name of the image from the
                product that is the closest match to the query.
        """

        product = proto.Field(
            proto.MESSAGE, number=1, message=product_search_service.Product,
        )
        score = proto.Field(proto.FLOAT, number=2,)
        image = proto.Field(proto.STRING, number=3,)

    category = proto.Field(proto.ENUM, number=1, enum="ProductSearchCategory",)
    product_category = proto.Field(proto.STRING, number=4,)
    index_time = proto.Field(proto.MESSAGE, number=2, message=timestamp_pb2.Timestamp,)
    products = proto.RepeatedField(proto.MESSAGE, number=3, message=ProductInfo,)
    results = proto.RepeatedField(proto.MESSAGE, number=5, message=Result,)


__all__ = tuple(sorted(__protobuf__.manifest))
