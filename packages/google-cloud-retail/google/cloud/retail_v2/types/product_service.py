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
from google.protobuf import timestamp_pb2  # type: ignore


__protobuf__ = proto.module(
    package="google.cloud.retail.v2",
    manifest={
        "CreateProductRequest",
        "GetProductRequest",
        "UpdateProductRequest",
        "DeleteProductRequest",
        "ListProductsRequest",
        "ListProductsResponse",
        "SetInventoryRequest",
        "SetInventoryMetadata",
        "SetInventoryResponse",
        "AddFulfillmentPlacesRequest",
        "AddFulfillmentPlacesMetadata",
        "AddFulfillmentPlacesResponse",
        "RemoveFulfillmentPlacesRequest",
        "RemoveFulfillmentPlacesMetadata",
        "RemoveFulfillmentPlacesResponse",
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
            does not exist and
            [allow_missing][google.cloud.retail.v2.UpdateProductRequest.allow_missing]
            is not set, a NOT_FOUND error is returned.
        update_mask (google.protobuf.field_mask_pb2.FieldMask):
            Indicates which fields in the provided
            [Product][google.cloud.retail.v2.Product] to update. The
            immutable and output only fields are NOT supported. If not
            set, all supported fields (the fields that are neither
            immutable nor output only) are updated.

            If an unsupported or unknown field is provided, an
            INVALID_ARGUMENT error is returned.
        allow_missing (bool):
            If set to true, and the
            [Product][google.cloud.retail.v2.Product] is not found, a
            new [Product][google.cloud.retail.v2.Product] will be
            created. In this situation, ``update_mask`` is ignored.
    """

    product = proto.Field(proto.MESSAGE, number=1, message=gcr_product.Product,)
    update_mask = proto.Field(
        proto.MESSAGE, number=2, message=field_mask_pb2.FieldMask,
    )
    allow_missing = proto.Field(proto.BOOL, number=3,)


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

            The [Product][google.cloud.retail.v2.Product] to delete can
            neither be a
            [Product.Type.COLLECTION][google.cloud.retail.v2.Product.Type.COLLECTION]
            [Product][google.cloud.retail.v2.Product] member nor a
            [Product.Type.PRIMARY][google.cloud.retail.v2.Product.Type.PRIMARY]
            [Product][google.cloud.retail.v2.Product] with more than one
            [variants][google.cloud.retail.v2.Product.Type.VARIANT].
            Otherwise, an INVALID_ARGUMENT error is returned.

            All inventory information for the named
            [Product][google.cloud.retail.v2.Product] will be deleted.
    """

    name = proto.Field(proto.STRING, number=1,)


class ListProductsRequest(proto.Message):
    r"""Request message for
    [ProductService.ListProducts][google.cloud.retail.v2.ProductService.ListProducts]
    method.

    Attributes:
        parent (str):
            Required. The parent branch resource name, such as
            ``projects/*/locations/global/catalogs/default_catalog/branches/0``.
            Use ``default_branch`` as the branch ID, to list products
            under the default branch.

            If the caller does not have permission to list
            [Product][google.cloud.retail.v2.Product]s under this
            branch, regardless of whether or not this branch exists, a
            PERMISSION_DENIED error is returned.
        page_size (int):
            Maximum number of [Product][google.cloud.retail.v2.Product]s
            to return. If unspecified, defaults to 100. The maximum
            allowed value is 1000. Values above 1000 will be coerced to
            1000.

            If this field is negative, an INVALID_ARGUMENT error is
            returned.
        page_token (str):
            A page token
            [ListProductsResponse.next_page_token][google.cloud.retail.v2.ListProductsResponse.next_page_token],
            received from a previous
            [ProductService.ListProducts][google.cloud.retail.v2.ProductService.ListProducts]
            call. Provide this to retrieve the subsequent page.

            When paginating, all other parameters provided to
            [ProductService.ListProducts][google.cloud.retail.v2.ProductService.ListProducts]
            must match the call that provided the page token. Otherwise,
            an INVALID_ARGUMENT error is returned.
        filter (str):
            A filter to apply on the list results. Supported features:

            -  List all the products under the parent branch if
               [filter][google.cloud.retail.v2.ListProductsRequest.filter]
               is unset.
            -  List
               [Product.Type.VARIANT][google.cloud.retail.v2.Product.Type.VARIANT]
               [Product][google.cloud.retail.v2.Product]s sharing the
               same
               [Product.Type.PRIMARY][google.cloud.retail.v2.Product.Type.PRIMARY]
               [Product][google.cloud.retail.v2.Product]. For example:
               ``primary_product_id = "some_product_id"``
            -  List [Product][google.cloud.retail.v2.Product]s bundled
               in a
               [Product.Type.COLLECTION][google.cloud.retail.v2.Product.Type.COLLECTION]
               [Product][google.cloud.retail.v2.Product]. For example:
               ``collection_product_id = "some_product_id"``
            -  List [Product][google.cloud.retail.v2.Product]s with a
               partibular type. For example: ``type = "PRIMARY"``
               ``type = "VARIANT"`` ``type = "COLLECTION"``

            If the field is unrecognizable, an INVALID_ARGUMENT error is
            returned.

            If the specified
            [Product.Type.PRIMARY][google.cloud.retail.v2.Product.Type.PRIMARY]
            [Product][google.cloud.retail.v2.Product] or
            [Product.Type.COLLECTION][google.cloud.retail.v2.Product.Type.COLLECTION]
            [Product][google.cloud.retail.v2.Product] does not exist, a
            NOT_FOUND error is returned.
        read_mask (google.protobuf.field_mask_pb2.FieldMask):
            The fields of [Product][google.cloud.retail.v2.Product] to
            return in the responses. If not set or empty, the following
            fields are returned:

            -  [Product.name][google.cloud.retail.v2.Product.name]
            -  [Product.id][google.cloud.retail.v2.Product.id]
            -  [Product.title][google.cloud.retail.v2.Product.title]
            -  [Product.uri][google.cloud.retail.v2.Product.uri]
            -  [Product.images][google.cloud.retail.v2.Product.images]
            -  [Product.price_info][google.cloud.retail.v2.Product.price_info]
            -  [Product.brands][google.cloud.retail.v2.Product.brands]

            If "*" is provided, all fields are returned.
            [Product.name][google.cloud.retail.v2.Product.name] is
            always returned no matter what mask is set.

            If an unsupported or unknown field is provided, an
            INVALID_ARGUMENT error is returned.
    """

    parent = proto.Field(proto.STRING, number=1,)
    page_size = proto.Field(proto.INT32, number=2,)
    page_token = proto.Field(proto.STRING, number=3,)
    filter = proto.Field(proto.STRING, number=4,)
    read_mask = proto.Field(proto.MESSAGE, number=5, message=field_mask_pb2.FieldMask,)


class ListProductsResponse(proto.Message):
    r"""Response message for
    [ProductService.ListProducts][google.cloud.retail.v2.ProductService.ListProducts]
    method.

    Attributes:
        products (Sequence[google.cloud.retail_v2.types.Product]):
            The [Product][google.cloud.retail.v2.Product]s.
        next_page_token (str):
            A token that can be sent as
            [ListProductsRequest.page_token][google.cloud.retail.v2.ListProductsRequest.page_token]
            to retrieve the next page. If this field is omitted, there
            are no subsequent pages.
    """

    @property
    def raw_page(self):
        return self

    products = proto.RepeatedField(
        proto.MESSAGE, number=1, message=gcr_product.Product,
    )
    next_page_token = proto.Field(proto.STRING, number=2,)


class SetInventoryRequest(proto.Message):
    r"""Request message for [SetInventory][] method.
    Attributes:
        inventory (google.cloud.retail_v2.types.Product):
            Required. The inventory information to update. The allowable
            fields to update are:

            -  [Product.price_info][google.cloud.retail.v2.Product.price_info]
            -  [Product.availability][google.cloud.retail.v2.Product.availability]
            -  [Product.available_quantity][google.cloud.retail.v2.Product.available_quantity]
            -  [Product.fulfillment_info][google.cloud.retail.v2.Product.fulfillment_info]
               The updated inventory fields must be specified in
               [SetInventoryRequest.set_mask][google.cloud.retail.v2.SetInventoryRequest.set_mask].

            If [SetInventoryRequest.inventory.name][] is empty or
            invalid, an INVALID_ARGUMENT error is returned.

            If the caller does not have permission to update the
            [Product][google.cloud.retail.v2.Product] named in
            [Product.name][google.cloud.retail.v2.Product.name],
            regardless of whether or not it exists, a PERMISSION_DENIED
            error is returned.

            If the [Product][google.cloud.retail.v2.Product] to update
            does not have existing inventory information, the provided
            inventory information will be inserted.

            If the [Product][google.cloud.retail.v2.Product] to update
            has existing inventory information, the provided inventory
            information will be merged while respecting the last update
            time for each inventory field, using the provided or default
            value for
            [SetInventoryRequest.set_time][google.cloud.retail.v2.SetInventoryRequest.set_time].

            The last update time is recorded for the following inventory
            fields:

            -  [Product.price_info][google.cloud.retail.v2.Product.price_info]
            -  [Product.availability][google.cloud.retail.v2.Product.availability]
            -  [Product.available_quantity][google.cloud.retail.v2.Product.available_quantity]
            -  [Product.fulfillment_info][google.cloud.retail.v2.Product.fulfillment_info]

            If a full overwrite of inventory information while ignoring
            timestamps is needed, [UpdateProduct][] should be invoked
            instead.
        set_mask (google.protobuf.field_mask_pb2.FieldMask):
            Indicates which inventory fields in the provided
            [Product][google.cloud.retail.v2.Product] to update. If not
            set or set with empty paths, all inventory fields will be
            updated.

            If an unsupported or unknown field is provided, an
            INVALID_ARGUMENT error is returned and the entire update
            will be ignored.
        set_time (google.protobuf.timestamp_pb2.Timestamp):
            The time when the request is issued, used to
            prevent out-of-order updates on inventory fields
            with the last update time recorded. If not
            provided, the internal system time will be used.
        allow_missing (bool):
            If set to true, and the
            [Product][google.cloud.retail.v2.Product] with name
            [Product.name][google.cloud.retail.v2.Product.name] is not
            found, the inventory update will still be processed and
            retained for at most 1 day until the
            [Product][google.cloud.retail.v2.Product] is created. If set
            to false, an INVALID_ARGUMENT error is returned if the
            [Product][google.cloud.retail.v2.Product] is not found.
    """

    inventory = proto.Field(proto.MESSAGE, number=1, message=gcr_product.Product,)
    set_mask = proto.Field(proto.MESSAGE, number=2, message=field_mask_pb2.FieldMask,)
    set_time = proto.Field(proto.MESSAGE, number=3, message=timestamp_pb2.Timestamp,)
    allow_missing = proto.Field(proto.BOOL, number=4,)


class SetInventoryMetadata(proto.Message):
    r"""Metadata related to the progress of the SetInventory operation.
    Currently empty because there is no meaningful metadata populated
    from the [SetInventory][] method.
        """


class SetInventoryResponse(proto.Message):
    r"""Response of the SetInventoryRequest. Currently empty because there
    is no meaningful response populated from the [SetInventory][]
    method.
        """


class AddFulfillmentPlacesRequest(proto.Message):
    r"""Request message for [AddFulfillmentPlaces][] method.
    Attributes:
        product (str):
            Required. Full resource name of
            [Product][google.cloud.retail.v2.Product], such as
            ``projects/*/locations/global/catalogs/default_catalog/branches/default_branch/products/some_product_id``.

            If the caller does not have permission to access the
            [Product][google.cloud.retail.v2.Product], regardless of
            whether or not it exists, a PERMISSION_DENIED error is
            returned.
        type_ (str):
            Required. The fulfillment type, including commonly used
            types (such as pickup in store and same day delivery), and
            custom types.

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

            This field directly corresponds to
            [Product.fulfillment_info.type][].
        place_ids (Sequence[str]):
            Required. The IDs for this
            [type][google.cloud.retail.v2.AddFulfillmentPlacesRequest.type],
            such as the store IDs for "pickup-in-store" or the region
            IDs for "same-day-delivery" to be added for this
            [type][google.cloud.retail.v2.AddFulfillmentPlacesRequest.type].
            Duplicate IDs will be automatically ignored.

            At least 1 value is required, and a maximum of 2000 values
            are allowed. Each value must be a string with a length limit
            of 10 characters, matching the pattern [a-zA-Z0-9\_-]+, such
            as "store1" or "REGION-2". Otherwise, an INVALID_ARGUMENT
            error is returned.

            If the total number of place IDs exceeds 2000 for this
            [type][google.cloud.retail.v2.AddFulfillmentPlacesRequest.type]
            after adding, then the update will be rejected.
        add_time (google.protobuf.timestamp_pb2.Timestamp):
            The time when the fulfillment updates are
            issued, used to prevent out-of-order updates on
            fulfillment information. If not provided, the
            internal system time will be used.
        allow_missing (bool):
            If set to true, and the
            [Product][google.cloud.retail.v2.Product] is not found, the
            fulfillment information will still be processed and retained
            for at most 1 day and processed once the
            [Product][google.cloud.retail.v2.Product] is created. If set
            to false, an INVALID_ARGUMENT error is returned if the
            [Product][google.cloud.retail.v2.Product] is not found.
    """

    product = proto.Field(proto.STRING, number=1,)
    type_ = proto.Field(proto.STRING, number=2,)
    place_ids = proto.RepeatedField(proto.STRING, number=3,)
    add_time = proto.Field(proto.MESSAGE, number=4, message=timestamp_pb2.Timestamp,)
    allow_missing = proto.Field(proto.BOOL, number=5,)


class AddFulfillmentPlacesMetadata(proto.Message):
    r"""Metadata related to the progress of the AddFulfillmentPlaces
    operation. Currently empty because there is no meaningful metadata
    populated from the [AddFulfillmentPlaces][] method.
        """


class AddFulfillmentPlacesResponse(proto.Message):
    r"""Response of the RemoveFulfillmentPlacesRequest. Currently empty
    because there is no meaningful response populated from the
    [AddFulfillmentPlaces][] method.
        """


class RemoveFulfillmentPlacesRequest(proto.Message):
    r"""Request message for [RemoveFulfillmentPlaces][] method.
    Attributes:
        product (str):
            Required. Full resource name of
            [Product][google.cloud.retail.v2.Product], such as
            ``projects/*/locations/global/catalogs/default_catalog/branches/default_branch/products/some_product_id``.

            If the caller does not have permission to access the
            [Product][google.cloud.retail.v2.Product], regardless of
            whether or not it exists, a PERMISSION_DENIED error is
            returned.
        type_ (str):
            Required. The fulfillment type, including commonly used
            types (such as pickup in store and same day delivery), and
            custom types.

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

            This field directly corresponds to
            [Product.fulfillment_info.type][].
        place_ids (Sequence[str]):
            Required. The IDs for this
            [type][google.cloud.retail.v2.RemoveFulfillmentPlacesRequest.type],
            such as the store IDs for "pickup-in-store" or the region
            IDs for "same-day-delivery", to be removed for this
            [type][google.cloud.retail.v2.RemoveFulfillmentPlacesRequest.type].

            At least 1 value is required, and a maximum of 2000 values
            are allowed. Each value must be a string with a length limit
            of 10 characters, matching the pattern [a-zA-Z0-9\_-]+, such
            as "store1" or "REGION-2". Otherwise, an INVALID_ARGUMENT
            error is returned.
        remove_time (google.protobuf.timestamp_pb2.Timestamp):
            The time when the fulfillment updates are
            issued, used to prevent out-of-order updates on
            fulfillment information. If not provided, the
            internal system time will be used.
        allow_missing (bool):
            If set to true, and the
            [Product][google.cloud.retail.v2.Product] is not found, the
            fulfillment information will still be processed and retained
            for at most 1 day and processed once the
            [Product][google.cloud.retail.v2.Product] is created. If set
            to false, an INVALID_ARGUMENT error is returned if the
            [Product][google.cloud.retail.v2.Product] is not found.
    """

    product = proto.Field(proto.STRING, number=1,)
    type_ = proto.Field(proto.STRING, number=2,)
    place_ids = proto.RepeatedField(proto.STRING, number=3,)
    remove_time = proto.Field(proto.MESSAGE, number=4, message=timestamp_pb2.Timestamp,)
    allow_missing = proto.Field(proto.BOOL, number=5,)


class RemoveFulfillmentPlacesMetadata(proto.Message):
    r"""Metadata related to the progress of the RemoveFulfillmentPlaces
    operation. Currently empty because there is no meaningful metadata
    populated from the [RemoveFulfillmentPlaces][] method.
        """


class RemoveFulfillmentPlacesResponse(proto.Message):
    r"""Response of the RemoveFulfillmentPlacesRequest. Currently empty
    because there is no meaningful response populated from the
    [RemoveFulfillmentPlaces][] method.
        """


__all__ = tuple(sorted(__protobuf__.manifest))
