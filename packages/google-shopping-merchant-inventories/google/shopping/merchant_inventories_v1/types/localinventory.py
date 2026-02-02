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

from google.shopping.merchant_inventories_v1.types import inventories_common

__protobuf__ = proto.module(
    package="google.shopping.merchant.inventories.v1",
    manifest={
        "LocalInventory",
        "ListLocalInventoriesRequest",
        "ListLocalInventoriesResponse",
        "InsertLocalInventoryRequest",
        "DeleteLocalInventoryRequest",
    },
)


class LocalInventory(proto.Message):
    r"""Local inventory information for the product. Represents in-store
    information for a specific product at the store specified by
    [``storeCode``][google.shopping.merchant.inventories.v1.LocalInventory.store_code].
    For a list of all accepted attribute values, see the `local product
    inventory data
    specification <https://support.google.com/merchants/answer/3061342>`__.

    Attributes:
        name (str):
            Output only. The name of the ``LocalInventory`` resource.
            Format:
            ``accounts/{account}/products/{product}/localInventories/{store_code}``
        account (int):
            Output only. The account that owns the
            product. This field will be ignored if set by
            the client.
        store_code (str):
            Required. Immutable. Store code (the store ID from your
            Business Profile) of the physical store the product is sold
            in. See the `Local product inventory data
            specification <https://support.google.com/merchants/answer/3061342>`__
            for more information.
        local_inventory_attributes (google.shopping.merchant_inventories_v1.types.LocalInventoryAttributes):
            Optional. A list of local inventory
            attributes.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    account: int = proto.Field(
        proto.INT64,
        number=2,
    )
    store_code: str = proto.Field(
        proto.STRING,
        number=3,
    )
    local_inventory_attributes: inventories_common.LocalInventoryAttributes = (
        proto.Field(
            proto.MESSAGE,
            number=14,
            message=inventories_common.LocalInventoryAttributes,
        )
    )


class ListLocalInventoriesRequest(proto.Message):
    r"""Request message for the ``ListLocalInventories`` method.

    Attributes:
        parent (str):
            Required. The ``name`` of the parent product to list local
            inventories for. Format:
            ``accounts/{account}/products/{product}``
        page_size (int):
            The maximum number of ``LocalInventory`` resources for the
            given product to return. The service returns fewer than this
            value if the number of inventories for the given product is
            less that than the ``pageSize``. The default value is 25000.
            The maximum value is 25000; If a value higher than the
            maximum is specified, then the ``pageSize`` will default to
            the maximum
        page_token (str):
            A page token, received from a previous
            ``ListLocalInventories`` call. Provide the page token to
            retrieve the subsequent page.

            When paginating, all other parameters provided to
            ``ListLocalInventories`` must match the call that provided
            the page token. The token returned as
            [nextPageToken][google.shopping.merchant.inventories.v1.ListLocalInventoriesResponse.next_page_token]
            in the response to the previous request.
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


class ListLocalInventoriesResponse(proto.Message):
    r"""Response message for the ``ListLocalInventories`` method.

    Attributes:
        local_inventories (MutableSequence[google.shopping.merchant_inventories_v1.types.LocalInventory]):
            The ``LocalInventory`` resources for the given product from
            the specified account.
        next_page_token (str):
            A token, which can be sent as ``pageToken`` to retrieve the
            next page. If this field is omitted, there are no subsequent
            pages.
    """

    @property
    def raw_page(self):
        return self

    local_inventories: MutableSequence["LocalInventory"] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="LocalInventory",
    )
    next_page_token: str = proto.Field(
        proto.STRING,
        number=2,
    )


class InsertLocalInventoryRequest(proto.Message):
    r"""Request message for the ``InsertLocalInventory`` method.

    Attributes:
        parent (str):
            Required. The account and product where this inventory will
            be inserted. Format:
            ``accounts/{account}/products/{product}``
        local_inventory (google.shopping.merchant_inventories_v1.types.LocalInventory):
            Required. Local inventory information of the product. If the
            product already has a ``LocalInventory`` resource for the
            same ``storeCode``, full replacement of the
            ``LocalInventory`` resource is performed.
    """

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    local_inventory: "LocalInventory" = proto.Field(
        proto.MESSAGE,
        number=2,
        message="LocalInventory",
    )


class DeleteLocalInventoryRequest(proto.Message):
    r"""Request message for the ``DeleteLocalInventory`` method.

    Attributes:
        name (str):
            Required. The name of the local inventory for the given
            product to delete. Format:
            ``accounts/{account}/products/{product}/localInventories/{store_code}``
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
