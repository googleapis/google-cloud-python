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

__protobuf__ = proto.module(
    package="google.ads.admanager.v1",
    manifest={
        "AdPartnerDeclaration",
        "DeclarationTypeEnum",
    },
)


class AdPartnerDeclaration(proto.Message):
    r"""Represents a set of declarations about what (if any) ad
    partners are associated with a given creative. This can be set
    at the network level, as a default for all creatives, or
    overridden for a particular creative.

    Attributes:
        type_ (google.ads.admanager_v1.types.DeclarationTypeEnum.DeclarationType):
            They type of declaration.
        ad_partners (MutableSequence[str]):
            The resource names of AdPartners being declared. Format:
            "networks/{network_code}/adPartners/{ad_partner_id}".
    """

    type_: "DeclarationTypeEnum.DeclarationType" = proto.Field(
        proto.ENUM,
        number=1,
        enum="DeclarationTypeEnum.DeclarationType",
    )
    ad_partners: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=2,
    )


class DeclarationTypeEnum(proto.Message):
    r"""Wrapper message for
    [DeclarationTypeEnum][google.ads.admanager.v1.DeclarationTypeEnum].

    """

    class DeclarationType(proto.Enum):
        r"""The declaration about third party data usage on the
        associated entity.

        Values:
            DECLARATION_TYPE_UNSPECIFIED (0):
                Default value. This value is unused.
            NONE (1):
                No ad technology providers to declare.
            DECLARED (2):
                There are are ad technology providers to
                declare on this entity.
        """
        DECLARATION_TYPE_UNSPECIFIED = 0
        NONE = 1
        DECLARED = 2


__all__ = tuple(sorted(__protobuf__.manifest))
