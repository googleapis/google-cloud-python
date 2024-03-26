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

from google.ads.admanager_v1.types import custom_field_enums

__protobuf__ = proto.module(
    package="google.ads.admanager.v1",
    manifest={
        "CustomField",
        "CustomFieldOption",
        "GetCustomFieldRequest",
        "ListCustomFieldsRequest",
        "ListCustomFieldsResponse",
    },
)


class CustomField(proto.Message):
    r"""The ``CustomField`` resource.

    Attributes:
        name (str):
            Identifier. The resource name of the ``CustomField``.
            Format:
            ``networks/{network_code}/customFields/{custom_field_id}``
        custom_field_id (int):
            Output only. ``CustomField`` ID.
        display_name (str):
            Required. The display name of the ``CustomField``.

            This value has a maximum length of 127 characters.
        description (str):
            Optional. The description of the ``CustomField``.

            This value has a maximum length of 511 characters.
        status (google.ads.admanager_v1.types.CustomFieldStatusEnum.CustomFieldStatus):
            Output only. The status of the ``CustomField``.
        entity_type (google.ads.admanager_v1.types.CustomFieldEntityTypeEnum.CustomFieldEntityType):
            Required. The type of entity the ``CustomField`` can be
            applied to.
        data_type (google.ads.admanager_v1.types.CustomFieldDataTypeEnum.CustomFieldDataType):
            Required. The data type of the ``CustomField``.
        visibility (google.ads.admanager_v1.types.CustomFieldVisibilityEnum.CustomFieldVisibility):
            Required. The visibility of the ``CustomField``.
        options (MutableSequence[google.ads.admanager_v1.types.CustomFieldOption]):
            Optional. The drop-down options for the ``CustomField``.

            Only applicable for ``CustomField`` with the drop-down data
            type.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    custom_field_id: int = proto.Field(
        proto.INT64,
        number=2,
    )
    display_name: str = proto.Field(
        proto.STRING,
        number=3,
    )
    description: str = proto.Field(
        proto.STRING,
        number=4,
    )
    status: custom_field_enums.CustomFieldStatusEnum.CustomFieldStatus = proto.Field(
        proto.ENUM,
        number=5,
        enum=custom_field_enums.CustomFieldStatusEnum.CustomFieldStatus,
    )
    entity_type: custom_field_enums.CustomFieldEntityTypeEnum.CustomFieldEntityType = (
        proto.Field(
            proto.ENUM,
            number=7,
            enum=custom_field_enums.CustomFieldEntityTypeEnum.CustomFieldEntityType,
        )
    )
    data_type: custom_field_enums.CustomFieldDataTypeEnum.CustomFieldDataType = (
        proto.Field(
            proto.ENUM,
            number=8,
            enum=custom_field_enums.CustomFieldDataTypeEnum.CustomFieldDataType,
        )
    )
    visibility: custom_field_enums.CustomFieldVisibilityEnum.CustomFieldVisibility = (
        proto.Field(
            proto.ENUM,
            number=9,
            enum=custom_field_enums.CustomFieldVisibilityEnum.CustomFieldVisibility,
        )
    )
    options: MutableSequence["CustomFieldOption"] = proto.RepeatedField(
        proto.MESSAGE,
        number=10,
        message="CustomFieldOption",
    )


class CustomFieldOption(proto.Message):
    r"""An option for a drop-down ``CustomField``.

    Attributes:
        custom_field_option_id (int):
            Output only. ``CustomFieldOption`` ID.
        display_name (str):
            Required. The display name of the ``CustomFieldOption``.

            This value has a maximum length of 127 characters.
    """

    custom_field_option_id: int = proto.Field(
        proto.INT64,
        number=1,
    )
    display_name: str = proto.Field(
        proto.STRING,
        number=2,
    )


class GetCustomFieldRequest(proto.Message):
    r"""Request object for ``GetCustomField`` method.

    Attributes:
        name (str):
            Required. The resource name of the CustomField. Format:
            ``networks/{network_code}/customFields/{custom_field_id}``
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class ListCustomFieldsRequest(proto.Message):
    r"""Request object for ``ListCustomFields`` method.

    Attributes:
        parent (str):
            Required. The parent, which owns this collection of
            CustomFields. Format: ``networks/{network_code}``
        page_size (int):
            Optional. The maximum number of ``CustomFields`` to return.
            The service may return fewer than this value. If
            unspecified, at most 50 ``CustomFields`` will be returned.
            The maximum value is 1000; values above 1000 will be coerced
            to 1000.
        page_token (str):
            Optional. A page token, received from a previous
            ``ListCustomFields`` call. Provide this to retrieve the
            subsequent page.

            When paginating, all other parameters provided to
            ``ListCustomFields`` must match the call that provided the
            page token.
        filter (str):
            Optional. Expression to filter the response.
            See syntax details at https://google.aip.dev/160
        order_by (str):
            Optional. Expression to specify sorting
            order. See syntax details at
            https://google.aip.dev/132#ordering
        skip (int):
            Optional. Number of individual resources to
            skip while paginating.
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
    filter: str = proto.Field(
        proto.STRING,
        number=4,
    )
    order_by: str = proto.Field(
        proto.STRING,
        number=5,
    )
    skip: int = proto.Field(
        proto.INT32,
        number=6,
    )


class ListCustomFieldsResponse(proto.Message):
    r"""Response object for ``ListCustomFieldsRequest`` containing matching
    ``CustomField`` objects.

    Attributes:
        custom_fields (MutableSequence[google.ads.admanager_v1.types.CustomField]):
            The ``CustomField`` objects from the specified network.
        next_page_token (str):
            A token, which can be sent as ``page_token`` to retrieve the
            next page. If this field is omitted, there are no subsequent
            pages.
        total_size (int):
            Total number of ``CustomField`` objects. If a filter was
            included in the request, this reflects the total number
            after the filtering is applied.

            ``total_size`` will not be calculated in the response unless
            it has been included in a response field mask. The response
            field mask can be provided to the method by using the URL
            parameter ``$fields`` or ``fields``, or by using the
            HTTP/gRPC header ``X-Goog-FieldMask``.

            For more information, see `System
            Parameters <https://cloud.google.com/apis/docs/system-parameters>`__.
    """

    @property
    def raw_page(self):
        return self

    custom_fields: MutableSequence["CustomField"] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="CustomField",
    )
    next_page_token: str = proto.Field(
        proto.STRING,
        number=2,
    )
    total_size: int = proto.Field(
        proto.INT32,
        number=3,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
