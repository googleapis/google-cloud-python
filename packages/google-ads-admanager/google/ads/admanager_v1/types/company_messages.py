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

from google.protobuf import timestamp_pb2  # type: ignore
import proto  # type: ignore

from google.ads.admanager_v1.types import applied_label, company_enums

__protobuf__ = proto.module(
    package="google.ads.admanager.v1",
    manifest={
        "Company",
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
            Optional. The credit status of the ``Company``.

            This attribute defaults to ``ACTIVE`` if basic settings are
            enabled and ``ON_HOLD`` if advance settings are enabled.
        applied_labels (MutableSequence[google.ads.admanager_v1.types.AppliedLabel]):
            Optional. The labels that are directly applied to the
            ``Company``.
        primary_contact (str):
            Optional. The resource names of primary Contact of the
            ``Company``. Format:
            "networks/{network_code}/contacts/{contact_id}".

            This field is a member of `oneof`_ ``_primary_contact``.
        applied_teams (MutableSequence[str]):
            Optional. The resource names of Teams that are directly
            associated with the ``Company``. Format:
            "networks/{network_code}/teams/{team_id}".
        third_party_company_id (int):
            Optional. The ID of the Google-recognized canonicalized form
            of the ``Company``.
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time the ``Company`` was last modified.
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
    type_: company_enums.CompanyTypeEnum.CompanyType = proto.Field(
        proto.ENUM,
        number=4,
        enum=company_enums.CompanyTypeEnum.CompanyType,
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
    credit_status: company_enums.CompanyCreditStatusEnum.CompanyCreditStatus = (
        proto.Field(
            proto.ENUM,
            number=11,
            enum=company_enums.CompanyCreditStatusEnum.CompanyCreditStatus,
        )
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
    third_party_company_id: int = proto.Field(
        proto.INT64,
        number=16,
    )
    update_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=15,
        message=timestamp_pb2.Timestamp,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
