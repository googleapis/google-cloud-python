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

from google.ads.admanager_v1.types import (
    applied_label,
    company_credit_status_enum,
    company_type_enum,
)

__protobuf__ = proto.module(
    package="google.ads.admanager.v1",
    manifest={
        "Company",
        "GetCompanyRequest",
        "ListCompaniesRequest",
        "ListCompaniesResponse",
    },
)


class Company(proto.Message):
    r"""The ``Company`` resource.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        name (str):
            Identifier. The resource name of the ``Company``. Format:
            ``networks/{network_code}/companies/{company_id}``
        company_id (int):
            Output only. ``Company`` ID.
        display_name (str):
            Required. The display name of the ``Company``.

            This value has a maximum length of 127 characters.
        type_ (google.ads.admanager_v1.types.CompanyTypeEnum.CompanyType):
            Required. The type of the ``Company``.
        address (str):
            Optional. The address for the ``Company``.

            This value has a maximum length of 1024 characters.
        email (str):
            Optional. The email for the ``Company``.

            This value has a maximum length of 128 characters.
        fax (str):
            Optional. The fax number for the ``Company``.

            This value has a maximum length of 63 characters.
        phone (str):
            Optional. The phone number for the ``Company``.

            This value has a maximum length of 63 characters.
        external_id (str):
            Optional. The external ID for the ``Company``.

            This value has a maximum length of 255 characters.
        comment (str):
            Optional. Comments about the ``Company``.

            This value has a maximum length of 1024 characters.
        credit_status (google.ads.admanager_v1.types.CompanyCreditStatusEnum.CompanyCreditStatus):
            Optional. The credit status of this company.

            This attribute defaults to ``ACTIVE`` if basic settings are
            enabled and ``ON_HOLD`` if advance settings are enabled.
        applied_labels (MutableSequence[google.ads.admanager_v1.types.AppliedLabel]):
            Optional. The labels that are directly
            applied to this company.
        primary_contact (str):
            Optional. The resource names of primary Contact of this
            company. Format:
            "networks/{network_code}/contacts/{contact_id}".

            This field is a member of `oneof`_ ``_primary_contact``.
        applied_teams (MutableSequence[str]):
            Optional. The resource names of Teams that are directly
            associated with this company. Format:
            "networks/{network_code}/teams/{team_id}".
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    company_id: int = proto.Field(
        proto.INT64,
        number=2,
    )
    display_name: str = proto.Field(
        proto.STRING,
        number=3,
    )
    type_: company_type_enum.CompanyTypeEnum.CompanyType = proto.Field(
        proto.ENUM,
        number=4,
        enum=company_type_enum.CompanyTypeEnum.CompanyType,
    )
    address: str = proto.Field(
        proto.STRING,
        number=5,
    )
    email: str = proto.Field(
        proto.STRING,
        number=6,
    )
    fax: str = proto.Field(
        proto.STRING,
        number=7,
    )
    phone: str = proto.Field(
        proto.STRING,
        number=8,
    )
    external_id: str = proto.Field(
        proto.STRING,
        number=9,
    )
    comment: str = proto.Field(
        proto.STRING,
        number=10,
    )
    credit_status: company_credit_status_enum.CompanyCreditStatusEnum.CompanyCreditStatus = proto.Field(
        proto.ENUM,
        number=11,
        enum=company_credit_status_enum.CompanyCreditStatusEnum.CompanyCreditStatus,
    )
    applied_labels: MutableSequence[applied_label.AppliedLabel] = proto.RepeatedField(
        proto.MESSAGE,
        number=12,
        message=applied_label.AppliedLabel,
    )
    primary_contact: str = proto.Field(
        proto.STRING,
        number=13,
        optional=True,
    )
    applied_teams: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=14,
    )


class GetCompanyRequest(proto.Message):
    r"""Request object for ``GetCompany`` method.

    Attributes:
        name (str):
            Required. The resource name of the Company. Format:
            ``networks/{network_code}/companies/{company_id}``
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class ListCompaniesRequest(proto.Message):
    r"""Request object for ``ListCompanies`` method.

    Attributes:
        parent (str):
            Required. The parent, which owns this collection of
            Companies. Format: ``networks/{network_code}``
        page_size (int):
            Optional. The maximum number of ``Companies`` to return. The
            service may return fewer than this value. If unspecified, at
            most 50 ``Companies`` will be returned. The maximum value is
            1000; values above 1000 will be coerced to 1000.
        page_token (str):
            Optional. A page token, received from a previous
            ``ListCompanies`` call. Provide this to retrieve the
            subsequent page.

            When paginating, all other parameters provided to
            ``ListCompanies`` must match the call that provided the page
            token.
        filter (str):
            Optional. Expression to filter the response.
            See syntax details at
            https://developers.google.com/ad-manager/api/beta/filters
        order_by (str):
            Optional. Expression to specify sorting
            order. See syntax details at
            https://developers.google.com/ad-manager/api/beta/filters#order
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


class ListCompaniesResponse(proto.Message):
    r"""Response object for ``ListCompaniesRequest`` containing matching
    ``Company`` resources.

    Attributes:
        companies (MutableSequence[google.ads.admanager_v1.types.Company]):
            The ``Company`` from the specified network.
        next_page_token (str):
            A token, which can be sent as ``page_token`` to retrieve the
            next page. If this field is omitted, there are no subsequent
            pages.
        total_size (int):
            Total number of ``Companies``. If a filter was included in
            the request, this reflects the total number after the
            filtering is applied.

            ``total_size`` will not be calculated in the response unless
            it has been included in a response field mask. The response
            field mask can be provided to the method by using the URL
            parameter ``$fields`` or ``fields``, or by using the
            HTTP/gRPC header ``X-Goog-FieldMask``.

            For more information, see
            https://developers.google.com/ad-manager/api/beta/field-masks
    """

    @property
    def raw_page(self):
        return self

    companies: MutableSequence["Company"] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="Company",
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
