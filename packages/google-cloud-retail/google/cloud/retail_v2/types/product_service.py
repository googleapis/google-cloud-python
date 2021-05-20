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

from google.cloud.retail_v2.types import product as gcr_product
from google.protobuf import field_mask_pb2  # type: ignore


__protobuf__ = proto.module(
    package="google.cloud.retail.v2",
    manifest={
        "CreateProductRequest",
        "GetProductRequest",
        "UpdateProductRequest",
        "DeleteProductRequest",
    },
)


class CreateProductRequest(proto.Message):
    r"""Request message for [CreateProduct][] method.
    Attributes:
        parent (str):
            Required. The parent catalog resource name, such as
            ``projects/*/locations/global/catalogs/default_catalog/branches/default_branch``.
        product (google.cloud.retail_v2.types.Product):
            Required. The [Product][google.cloud.retail.v2.Product] to
            create.
        product_id (str):
            Required. The ID to use for the
            [Product][google.cloud.retail.v2.Product], which will become
            the final component of the
            [Product.name][google.cloud.retail.v2.Product.name].

            If the caller does not have permission to create the
            [Product][google.cloud.retail.v2.Product], regardless of
            whether or not it exists, a PERMISSION_DENIED error is
            returned.

            This field must be unique among all
            [Product][google.cloud.retail.v2.Product]s with the same
            [parent][google.cloud.retail.v2.CreateProductRequest.parent].
            Otherwise, an ALREADY_EXISTS error is returned.

            This field must be a UTF-8 encoded string with a length
            limit of 128 characters. Otherwise, an INVALID_ARGUMENT
            error is returned.
    """

    parent = proto.Field(proto.STRING, number=1,)
    product = proto.Field(proto.MESSAGE, number=2, message=gcr_product.Product,)
    product_id = proto.Field(proto.STRING, number=3,)


class GetProductRequest(proto.Message):
    r"""Request message for [GetProduct][] method.
    Attributes:
        name (str):
            Required. Full resource name of
            [Product][google.cloud.retail.v2.Product], such as
            ``projects/*/locations/global/catalogs/default_catalog/branches/default_branch/products/some_product_id``.

            If the caller does not have permission to access the
            [Product][google.cloud.retail.v2.Product], regardless of
            whether or not it exists, a PERMISSION_DENIED error is
            returned.

            If the requested [Product][google.cloud.retail.v2.Product]
            does not exist, a NOT_FOUND error is returned.
    """

    name = proto.Field(proto.STRING, number=1,)


class UpdateProductRequest(proto.Message):
    r"""Request message for [UpdateProduct][] method.
    Attributes:
        product (google.cloud.retail_v2.types.Product):
            Required. The product to update/create.

            If the caller does not have permission to update the
            [Product][google.cloud.retail.v2.Product], regardless of
            whether or not it exists, a PERMISSION_DENIED error is
            returned.

            If the [Product][google.cloud.retail.v2.Product] to update
            does not exist, a NOT_FOUND error is returned.
        update_mask (google.protobuf.field_mask_pb2.FieldMask):
            Indicates which fields in the provided
            [Product][google.cloud.retail.v2.Product] to update. The
            immutable and output only fields are NOT supported. If not
            set, all supported fields (the fields that are neither
            immutable nor output only) are updated.

            If an unsupported or unknown field is provided, an
            INVALID_ARGUMENT error is returned.
    """

    product = proto.Field(proto.MESSAGE, number=1, message=gcr_product.Product,)
    update_mask = proto.Field(
        proto.MESSAGE, number=2, message=field_mask_pb2.FieldMask,
    )


class DeleteProductRequest(proto.Message):
    r"""Request message for [DeleteProduct][] method.
    Attributes:
        name (str):
            Required. Full resource name of
            [Product][google.cloud.retail.v2.Product], such as
            ``projects/*/locations/global/catalogs/default_catalog/branches/default_branch/products/some_product_id``.

            If the caller does not have permission to delete the
            [Product][google.cloud.retail.v2.Product], regardless of
            whether or not it exists, a PERMISSION_DENIED error is
            returned.

            If the [Product][google.cloud.retail.v2.Product] to delete
            does not exist, a NOT_FOUND error is returned.
    """

    name = proto.Field(proto.STRING, number=1,)


__all__ = tuple(sorted(__protobuf__.manifest))
