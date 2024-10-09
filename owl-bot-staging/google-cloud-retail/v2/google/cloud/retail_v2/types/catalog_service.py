# -*- coding: utf-8 -*-
# Copyright 2024 Google LLC
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

from google.cloud.retail_v2.types import catalog as gcr_catalog
from google.protobuf import field_mask_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore


__protobuf__ = proto.module(
    package='google.cloud.retail.v2',
    manifest={
        'ListCatalogsRequest',
        'ListCatalogsResponse',
        'UpdateCatalogRequest',
        'SetDefaultBranchRequest',
        'GetDefaultBranchRequest',
        'GetDefaultBranchResponse',
        'GetCompletionConfigRequest',
        'UpdateCompletionConfigRequest',
        'GetAttributesConfigRequest',
        'UpdateAttributesConfigRequest',
        'AddCatalogAttributeRequest',
        'RemoveCatalogAttributeRequest',
        'ReplaceCatalogAttributeRequest',
    },
)


class ListCatalogsRequest(proto.Message):
    r"""Request for
    [CatalogService.ListCatalogs][google.cloud.retail.v2.CatalogService.ListCatalogs]
    method.

    Attributes:
        parent (str):
            Required. The account resource name with an associated
            location.

            If the caller does not have permission to list
            [Catalog][google.cloud.retail.v2.Catalog]s under this
            location, regardless of whether or not this location exists,
            a PERMISSION_DENIED error is returned.
        page_size (int):
            Maximum number of [Catalog][google.cloud.retail.v2.Catalog]s
            to return. If unspecified, defaults to 50. The maximum
            allowed value is 1000. Values above 1000 will be coerced to
            1000.

            If this field is negative, an INVALID_ARGUMENT is returned.
        page_token (str):
            A page token
            [ListCatalogsResponse.next_page_token][google.cloud.retail.v2.ListCatalogsResponse.next_page_token],
            received from a previous
            [CatalogService.ListCatalogs][google.cloud.retail.v2.CatalogService.ListCatalogs]
            call. Provide this to retrieve the subsequent page.

            When paginating, all other parameters provided to
            [CatalogService.ListCatalogs][google.cloud.retail.v2.CatalogService.ListCatalogs]
            must match the call that provided the page token. Otherwise,
            an INVALID_ARGUMENT error is returned.
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


class ListCatalogsResponse(proto.Message):
    r"""Response for
    [CatalogService.ListCatalogs][google.cloud.retail.v2.CatalogService.ListCatalogs]
    method.

    Attributes:
        catalogs (MutableSequence[google.cloud.retail_v2.types.Catalog]):
            All the customer's
            [Catalog][google.cloud.retail.v2.Catalog]s.
        next_page_token (str):
            A token that can be sent as
            [ListCatalogsRequest.page_token][google.cloud.retail.v2.ListCatalogsRequest.page_token]
            to retrieve the next page. If this field is omitted, there
            are no subsequent pages.
    """

    @property
    def raw_page(self):
        return self

    catalogs: MutableSequence[gcr_catalog.Catalog] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message=gcr_catalog.Catalog,
    )
    next_page_token: str = proto.Field(
        proto.STRING,
        number=2,
    )


class UpdateCatalogRequest(proto.Message):
    r"""Request for
    [CatalogService.UpdateCatalog][google.cloud.retail.v2.CatalogService.UpdateCatalog]
    method.

    Attributes:
        catalog (google.cloud.retail_v2.types.Catalog):
            Required. The [Catalog][google.cloud.retail.v2.Catalog] to
            update.

            If the caller does not have permission to update the
            [Catalog][google.cloud.retail.v2.Catalog], regardless of
            whether or not it exists, a PERMISSION_DENIED error is
            returned.

            If the [Catalog][google.cloud.retail.v2.Catalog] to update
            does not exist, a NOT_FOUND error is returned.
        update_mask (google.protobuf.field_mask_pb2.FieldMask):
            Indicates which fields in the provided
            [Catalog][google.cloud.retail.v2.Catalog] to update.

            If an unsupported or unknown field is provided, an
            INVALID_ARGUMENT error is returned.
    """

    catalog: gcr_catalog.Catalog = proto.Field(
        proto.MESSAGE,
        number=1,
        message=gcr_catalog.Catalog,
    )
    update_mask: field_mask_pb2.FieldMask = proto.Field(
        proto.MESSAGE,
        number=2,
        message=field_mask_pb2.FieldMask,
    )


class SetDefaultBranchRequest(proto.Message):
    r"""Request message to set a specified branch as new default_branch.

    Attributes:
        catalog (str):
            Full resource name of the catalog, such as
            ``projects/*/locations/global/catalogs/default_catalog``.
        branch_id (str):
            The final component of the resource name of a branch.

            This field must be one of "0", "1" or "2". Otherwise, an
            INVALID_ARGUMENT error is returned.

            If there are no sufficient active products in the targeted
            branch and
            [force][google.cloud.retail.v2.SetDefaultBranchRequest.force]
            is not set, a FAILED_PRECONDITION error is returned.
        note (str):
            Some note on this request, this can be retrieved by
            [CatalogService.GetDefaultBranch][google.cloud.retail.v2.CatalogService.GetDefaultBranch]
            before next valid default branch set occurs.

            This field must be a UTF-8 encoded string with a length
            limit of 1,000 characters. Otherwise, an INVALID_ARGUMENT
            error is returned.
        force (bool):
            If set to true, it permits switching to a branch with
            [branch_id][google.cloud.retail.v2.SetDefaultBranchRequest.branch_id]
            even if it has no sufficient active products.
    """

    catalog: str = proto.Field(
        proto.STRING,
        number=1,
    )
    branch_id: str = proto.Field(
        proto.STRING,
        number=2,
    )
    note: str = proto.Field(
        proto.STRING,
        number=3,
    )
    force: bool = proto.Field(
        proto.BOOL,
        number=4,
    )


class GetDefaultBranchRequest(proto.Message):
    r"""Request message to show which branch is currently the default
    branch.

    Attributes:
        catalog (str):
            The parent catalog resource name, such as
            ``projects/*/locations/global/catalogs/default_catalog``.
    """

    catalog: str = proto.Field(
        proto.STRING,
        number=1,
    )


class GetDefaultBranchResponse(proto.Message):
    r"""Response message of
    [CatalogService.GetDefaultBranch][google.cloud.retail.v2.CatalogService.GetDefaultBranch].

    Attributes:
        branch (str):
            Full resource name of the branch id currently
            set as default branch.
        set_time (google.protobuf.timestamp_pb2.Timestamp):
            The time when this branch is set to default.
        note (str):
            This corresponds to
            [SetDefaultBranchRequest.note][google.cloud.retail.v2.SetDefaultBranchRequest.note]
            field, when this branch was set as default.
    """

    branch: str = proto.Field(
        proto.STRING,
        number=1,
    )
    set_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=2,
        message=timestamp_pb2.Timestamp,
    )
    note: str = proto.Field(
        proto.STRING,
        number=3,
    )


class GetCompletionConfigRequest(proto.Message):
    r"""Request for
    [CatalogService.GetCompletionConfig][google.cloud.retail.v2.CatalogService.GetCompletionConfig]
    method.

    Attributes:
        name (str):
            Required. Full CompletionConfig resource name. Format:
            ``projects/{project_number}/locations/{location_id}/catalogs/{catalog_id}/completionConfig``
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class UpdateCompletionConfigRequest(proto.Message):
    r"""Request for
    [CatalogService.UpdateCompletionConfig][google.cloud.retail.v2.CatalogService.UpdateCompletionConfig]
    method.

    Attributes:
        completion_config (google.cloud.retail_v2.types.CompletionConfig):
            Required. The
            [CompletionConfig][google.cloud.retail.v2.CompletionConfig]
            to update.

            If the caller does not have permission to update the
            [CompletionConfig][google.cloud.retail.v2.CompletionConfig],
            then a PERMISSION_DENIED error is returned.

            If the
            [CompletionConfig][google.cloud.retail.v2.CompletionConfig]
            to update does not exist, a NOT_FOUND error is returned.
        update_mask (google.protobuf.field_mask_pb2.FieldMask):
            Indicates which fields in the provided
            [CompletionConfig][google.cloud.retail.v2.CompletionConfig]
            to update. The following are the only supported fields:

            -  [CompletionConfig.matching_order][google.cloud.retail.v2.CompletionConfig.matching_order]
            -  [CompletionConfig.max_suggestions][google.cloud.retail.v2.CompletionConfig.max_suggestions]
            -  [CompletionConfig.min_prefix_length][google.cloud.retail.v2.CompletionConfig.min_prefix_length]
            -  [CompletionConfig.auto_learning][google.cloud.retail.v2.CompletionConfig.auto_learning]

            If not set, all supported fields are updated.
    """

    completion_config: gcr_catalog.CompletionConfig = proto.Field(
        proto.MESSAGE,
        number=1,
        message=gcr_catalog.CompletionConfig,
    )
    update_mask: field_mask_pb2.FieldMask = proto.Field(
        proto.MESSAGE,
        number=2,
        message=field_mask_pb2.FieldMask,
    )


class GetAttributesConfigRequest(proto.Message):
    r"""Request for
    [CatalogService.GetAttributesConfig][google.cloud.retail.v2.CatalogService.GetAttributesConfig]
    method.

    Attributes:
        name (str):
            Required. Full AttributesConfig resource name. Format:
            ``projects/{project_number}/locations/{location_id}/catalogs/{catalog_id}/attributesConfig``
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class UpdateAttributesConfigRequest(proto.Message):
    r"""Request for
    [CatalogService.UpdateAttributesConfig][google.cloud.retail.v2.CatalogService.UpdateAttributesConfig]
    method.

    Attributes:
        attributes_config (google.cloud.retail_v2.types.AttributesConfig):
            Required. The
            [AttributesConfig][google.cloud.retail.v2.AttributesConfig]
            to update.
        update_mask (google.protobuf.field_mask_pb2.FieldMask):
            Indicates which fields in the provided
            [AttributesConfig][google.cloud.retail.v2.AttributesConfig]
            to update. The following is the only supported field:

            -  [AttributesConfig.catalog_attributes][google.cloud.retail.v2.AttributesConfig.catalog_attributes]

            If not set, all supported fields are updated.
    """

    attributes_config: gcr_catalog.AttributesConfig = proto.Field(
        proto.MESSAGE,
        number=1,
        message=gcr_catalog.AttributesConfig,
    )
    update_mask: field_mask_pb2.FieldMask = proto.Field(
        proto.MESSAGE,
        number=2,
        message=field_mask_pb2.FieldMask,
    )


class AddCatalogAttributeRequest(proto.Message):
    r"""Request for
    [CatalogService.AddCatalogAttribute][google.cloud.retail.v2.CatalogService.AddCatalogAttribute]
    method.

    Attributes:
        attributes_config (str):
            Required. Full AttributesConfig resource name. Format:
            ``projects/{project_number}/locations/{location_id}/catalogs/{catalog_id}/attributesConfig``
        catalog_attribute (google.cloud.retail_v2.types.CatalogAttribute):
            Required. The
            [CatalogAttribute][google.cloud.retail.v2.CatalogAttribute]
            to add.
    """

    attributes_config: str = proto.Field(
        proto.STRING,
        number=1,
    )
    catalog_attribute: gcr_catalog.CatalogAttribute = proto.Field(
        proto.MESSAGE,
        number=2,
        message=gcr_catalog.CatalogAttribute,
    )


class RemoveCatalogAttributeRequest(proto.Message):
    r"""Request for
    [CatalogService.RemoveCatalogAttribute][google.cloud.retail.v2.CatalogService.RemoveCatalogAttribute]
    method.

    Attributes:
        attributes_config (str):
            Required. Full AttributesConfig resource name. Format:
            ``projects/{project_number}/locations/{location_id}/catalogs/{catalog_id}/attributesConfig``
        key (str):
            Required. The attribute name key of the
            [CatalogAttribute][google.cloud.retail.v2.CatalogAttribute]
            to remove.
    """

    attributes_config: str = proto.Field(
        proto.STRING,
        number=1,
    )
    key: str = proto.Field(
        proto.STRING,
        number=2,
    )


class ReplaceCatalogAttributeRequest(proto.Message):
    r"""Request for
    [CatalogService.ReplaceCatalogAttribute][google.cloud.retail.v2.CatalogService.ReplaceCatalogAttribute]
    method.

    Attributes:
        attributes_config (str):
            Required. Full AttributesConfig resource name. Format:
            ``projects/{project_number}/locations/{location_id}/catalogs/{catalog_id}/attributesConfig``
        catalog_attribute (google.cloud.retail_v2.types.CatalogAttribute):
            Required. The updated
            [CatalogAttribute][google.cloud.retail.v2.CatalogAttribute].
        update_mask (google.protobuf.field_mask_pb2.FieldMask):
            Indicates which fields in the provided
            [CatalogAttribute][google.cloud.retail.v2.CatalogAttribute]
            to update. The following are NOT supported:

            -  [CatalogAttribute.key][google.cloud.retail.v2.CatalogAttribute.key]

            If not set, all supported fields are updated.
    """

    attributes_config: str = proto.Field(
        proto.STRING,
        number=1,
    )
    catalog_attribute: gcr_catalog.CatalogAttribute = proto.Field(
        proto.MESSAGE,
        number=2,
        message=gcr_catalog.CatalogAttribute,
    )
    update_mask: field_mask_pb2.FieldMask = proto.Field(
        proto.MESSAGE,
        number=3,
        message=field_mask_pb2.FieldMask,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
