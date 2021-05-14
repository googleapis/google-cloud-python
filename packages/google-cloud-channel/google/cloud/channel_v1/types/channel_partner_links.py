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

from google.cloud.channel_v1.types import common
from google.protobuf import timestamp_pb2  # type: ignore


__protobuf__ = proto.module(
    package="google.cloud.channel.v1",
    manifest={
        "ChannelPartnerLinkView",
        "ChannelPartnerLinkState",
        "ChannelPartnerLink",
    },
)


class ChannelPartnerLinkView(proto.Enum):
    r"""The level of granularity the
    [ChannelPartnerLink][google.cloud.channel.v1.ChannelPartnerLink]
    will display.
    """
    UNSPECIFIED = 0
    BASIC = 1
    FULL = 2


class ChannelPartnerLinkState(proto.Enum):
    r"""ChannelPartnerLinkState represents state of a channel partner
    link.
    """
    CHANNEL_PARTNER_LINK_STATE_UNSPECIFIED = 0
    INVITED = 1
    ACTIVE = 2
    REVOKED = 3
    SUSPENDED = 4


class ChannelPartnerLink(proto.Message):
    r"""Entity representing a link between distributors and their
    indirect resellers in an n-tier resale channel.

    Attributes:
        name (str):
            Output only. Resource name for the channel partner link, in
            the format accounts/{account_id}/channelPartnerLinks/{id}.
        reseller_cloud_identity_id (str):
            Required. Cloud Identity ID of the linked
            reseller.
        link_state (google.cloud.channel_v1.types.ChannelPartnerLinkState):
            Required. State of the channel partner link.
        invite_link_uri (str):
            Output only. URI of the web page where
            partner accepts the link invitation.
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. Timestamp of when the channel
            partner link is created.
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. Timestamp of when the channel
            partner link is updated.
        public_id (str):
            Output only. Public identifier that a
            customer must use to generate a transfer token
            to move to this distributor-reseller
            combination.
        channel_partner_cloud_identity_info (google.cloud.channel_v1.types.CloudIdentityInfo):
            Output only. Cloud Identity info of the
            channel partner (IR).
    """

    name = proto.Field(proto.STRING, number=1,)
    reseller_cloud_identity_id = proto.Field(proto.STRING, number=2,)
    link_state = proto.Field(proto.ENUM, number=3, enum="ChannelPartnerLinkState",)
    invite_link_uri = proto.Field(proto.STRING, number=4,)
    create_time = proto.Field(proto.MESSAGE, number=5, message=timestamp_pb2.Timestamp,)
    update_time = proto.Field(proto.MESSAGE, number=6, message=timestamp_pb2.Timestamp,)
    public_id = proto.Field(proto.STRING, number=7,)
    channel_partner_cloud_identity_info = proto.Field(
        proto.MESSAGE, number=8, message=common.CloudIdentityInfo,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
