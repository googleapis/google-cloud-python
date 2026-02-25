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

from google.ads.datamanager_v1.types import consent as gad_consent
from google.ads.datamanager_v1.types import user_data as gad_user_data

__protobuf__ = proto.module(
    package="google.ads.datamanager.v1",
    manifest={
        "AudienceMember",
        "PairData",
        "MobileData",
        "UserIdData",
        "PpidData",
    },
)


class AudienceMember(proto.Message):
    r"""The audience member to be operated on.

    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        destination_references (MutableSequence[str]):
            Optional. Defines which
            [Destination][google.ads.datamanager.v1.Destination] to send
            the audience member to.
        user_data (google.ads.datamanager_v1.types.UserData):
            User-provided data that identifies the user.

            This field is a member of `oneof`_ ``data``.
        pair_data (google.ads.datamanager_v1.types.PairData):
            `Publisher Advertiser Identity Reconciliation (PAIR)
            IDs <//support.google.com/admanager/answer/15067908>`__.

            This feature is only available to data partners.

            This field is a member of `oneof`_ ``data``.
        mobile_data (google.ads.datamanager_v1.types.MobileData):
            Data identifying the user's mobile devices.

            This field is a member of `oneof`_ ``data``.
        user_id_data (google.ads.datamanager_v1.types.UserIdData):
            Data related to unique identifiers for a
            user, as defined by the advertiser.

            This field is a member of `oneof`_ ``data``.
        ppid_data (google.ads.datamanager_v1.types.PpidData):
            Data related to publisher provided
            identifiers.
            This feature is only available to data partners.

            This field is a member of `oneof`_ ``data``.
        consent (google.ads.datamanager_v1.types.Consent):
            Optional. The consent setting for the user.
    """

    destination_references: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=1,
    )
    user_data: gad_user_data.UserData = proto.Field(
        proto.MESSAGE,
        number=2,
        oneof="data",
        message=gad_user_data.UserData,
    )
    pair_data: "PairData" = proto.Field(
        proto.MESSAGE,
        number=4,
        oneof="data",
        message="PairData",
    )
    mobile_data: "MobileData" = proto.Field(
        proto.MESSAGE,
        number=5,
        oneof="data",
        message="MobileData",
    )
    user_id_data: "UserIdData" = proto.Field(
        proto.MESSAGE,
        number=6,
        oneof="data",
        message="UserIdData",
    )
    ppid_data: "PpidData" = proto.Field(
        proto.MESSAGE,
        number=7,
        oneof="data",
        message="PpidData",
    )
    consent: gad_consent.Consent = proto.Field(
        proto.MESSAGE,
        number=3,
        message=gad_consent.Consent,
    )


class PairData(proto.Message):
    r"""`PAIR <//support.google.com/admanager/answer/15067908>`__ IDs for
    the audience. At least one PAIR ID is required.

    This feature is only available to data partners.

    Attributes:
        pair_ids (MutableSequence[str]):
            Required. Cleanroom-provided PII data, hashed with SHA256,
            and encrypted with an EC commutative cipher using publisher
            key for the
            `PAIR <(//support.google.com/admanager/answer/15067908)>`__
            user list. At most 10 ``pairIds`` can be provided in a
            single
            [AudienceMember][google.ads.datamanager.v1.AudienceMember].
    """

    pair_ids: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=1,
    )


class MobileData(proto.Message):
    r"""Mobile IDs for the audience. At least one mobile ID is
    required.

    Attributes:
        mobile_ids (MutableSequence[str]):
            Required. The list of mobile device IDs (advertising
            ID/IDFA). At most 10 ``mobileIds`` can be provided in a
            single
            [AudienceMember][google.ads.datamanager.v1.AudienceMember].
    """

    mobile_ids: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=1,
    )


class UserIdData(proto.Message):
    r"""User id data holding the user id.

    Attributes:
        user_id (str):
            Required. A unique identifier for a user, as
            defined by the advertiser.
    """

    user_id: str = proto.Field(
        proto.STRING,
        number=1,
    )


class PpidData(proto.Message):
    r"""Publisher provided identifiers data holding the ppids. At
    least one ppid is required.

    This feature is only available to data partners.

    Attributes:
        ppids (MutableSequence[str]):
            Required. The list of publisher provided
            identifiers for a user.
    """

    ppids: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=1,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
