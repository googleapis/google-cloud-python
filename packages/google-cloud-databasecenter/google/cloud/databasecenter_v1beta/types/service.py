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

from google.cloud.databasecenter_v1beta.types import product

__protobuf__ = proto.module(
    package="google.cloud.databasecenter.v1beta",
    manifest={
        "QueryProductsRequest",
        "QueryProductsResponse",
    },
)


class QueryProductsRequest(proto.Message):
    r"""QueryProductsRequest is the request to get a list of
    products.

    Attributes:
        parent (str):
            Required. Parent can be a project, a folder, or an
            organization.

            The allowed values are:

            - projects/{PROJECT_ID}/locations/{LOCATION}
              (e.g.,"projects/foo-bar/locations/us-central1")
            - projects/{PROJECT_NUMBER}/locations/{LOCATION}
              (e.g.,"projects/12345678/locations/us-central1")
            - folders/{FOLDER_NUMBER}/locations/{LOCATION}
              (e.g.,"folders/1234567/locations/us-central1")
            - organizations/{ORGANIZATION_NUMBER}/locations/{LOCATION}
              (e.g.,"organizations/123456/locations/us-central1")
            - projects/{PROJECT_ID} (e.g., "projects/foo-bar")
            - projects/{PROJECT_NUMBER} (e.g., "projects/12345678")
            - folders/{FOLDER_NUMBER} (e.g., "folders/1234567")
            - organizations/{ORGANIZATION_NUMBER} (e.g.,
              "organizations/123456")
        page_size (int):
            Optional. If unspecified, at most 50 products
            will be returned. The maximum value is 1000;
            values above 1000 will be coerced to 1000.
        page_token (str):
            Optional. A page token, received from a previous
            ``ListLocations`` call. Provide this to retrieve the
            subsequent page. All other parameters except page size
            should match the call that provided the page page token.
    """

    parent: str = proto.Field(
        proto.STRING,
        number=3,
    )
    page_size: int = proto.Field(
        proto.INT32,
        number=1,
    )
    page_token: str = proto.Field(
        proto.STRING,
        number=2,
    )


class QueryProductsResponse(proto.Message):
    r"""QueryProductsResponse represents the response containing a
    list of products.

    Attributes:
        products (MutableSequence[google.cloud.databasecenter_v1beta.types.Product]):
            List of database products returned.
        next_page_token (str):
            A token that can be sent as ``page_token`` to retrieve the
            next page. If this field is omitted, there are no subsequent
            pages
        unreachable (MutableSequence[str]):
            Unordered list. List of unreachable regions
            from where data could not be retrieved.
    """

    @property
    def raw_page(self):
        return self

    products: MutableSequence[product.Product] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message=product.Product,
    )
    next_page_token: str = proto.Field(
        proto.STRING,
        number=2,
    )
    unreachable: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=3,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
