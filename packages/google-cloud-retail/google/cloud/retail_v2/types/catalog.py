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
    package="google.cloud.retail.v2", manifest={"ProductLevelConfig", "Catalog",},
)


class ProductLevelConfig(proto.Message):
    r"""Configures what level the product should be uploaded with
    regards to how users will be send events and how predictions
    will be made.

    Attributes:
        ingestion_product_type (str):
            The type of [Product][google.cloud.retail.v2.Product]s
            allowed to be ingested into the catalog. Acceptable values
            are:

            -  ``primary`` (default): You can only ingest
               [Product.Type.PRIMARY][google.cloud.retail.v2.Product.Type.PRIMARY]
               [Product][google.cloud.retail.v2.Product]s. This means
               [Product.primary_product_id][google.cloud.retail.v2.Product.primary_product_id]
               can only be empty or set to the same value as
               [Product.id][google.cloud.retail.v2.Product.id].
            -  ``variant``: You can only ingest
               [Product.Type.VARIANT][google.cloud.retail.v2.Product.Type.VARIANT]
               [Product][google.cloud.retail.v2.Product]s. This means
               [Product.primary_product_id][google.cloud.retail.v2.Product.primary_product_id]
               cannot be empty.

            If this field is set to an invalid value other than these,
            an INVALID_ARGUMENT error is returned.

            If this field is ``variant`` and
            [merchant_center_product_id_field][google.cloud.retail.v2.ProductLevelConfig.merchant_center_product_id_field]
            is ``itemGroupId``, an INVALID_ARGUMENT error is returned.

            See `Using catalog
            levels </retail/recommendations-ai/docs/catalog#catalog-levels>`__
            for more details.
        merchant_center_product_id_field (str):
            Which field of `Merchant Center
            Product </bigquery-transfer/docs/merchant-center-products-schema>`__
            should be imported as
            [Product.id][google.cloud.retail.v2.Product.id]. Acceptable
            values are:

            -  ``offerId`` (default): Import ``offerId`` as the product
               ID.
            -  ``itemGroupId``: Import ``itemGroupId`` as the product
               ID. Notice that Retail API will choose one item from the
               ones with the same ``itemGroupId``, and use it to
               represent the item group.

            If this field is set to an invalid value other than these,
            an INVALID_ARGUMENT error is returned.

            If this field is ``itemGroupId`` and
            [ingestion_product_type][google.cloud.retail.v2.ProductLevelConfig.ingestion_product_type]
            is ``variant``, an INVALID_ARGUMENT error is returned.

            See `Using catalog
            levels </retail/recommendations-ai/docs/catalog#catalog-levels>`__
            for more details.
    """

    ingestion_product_type = proto.Field(proto.STRING, number=1,)
    merchant_center_product_id_field = proto.Field(proto.STRING, number=2,)


class Catalog(proto.Message):
    r"""The catalog configuration.
    Attributes:
        name (str):
            Required. Immutable. The fully qualified
            resource name of the catalog.
        display_name (str):
            Required. Immutable. The catalog display name.

            This field must be a UTF-8 encoded string with a length
            limit of 128 characters. Otherwise, an INVALID_ARGUMENT
            error is returned.
        product_level_config (google.cloud.retail_v2.types.ProductLevelConfig):
            Required. The product level configuration.
    """

    name = proto.Field(proto.STRING, number=1,)
    display_name = proto.Field(proto.STRING, number=2,)
    product_level_config = proto.Field(
        proto.MESSAGE, number=4, message="ProductLevelConfig",
    )


__all__ = tuple(sorted(__protobuf__.manifest))
