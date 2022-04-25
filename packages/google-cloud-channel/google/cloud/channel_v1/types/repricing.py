# -*- coding: utf-8 -*-
# Copyright 2022 Google LLC
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
from google.protobuf import timestamp_pb2  # type: ignore
from google.type import date_pb2  # type: ignore
from google.type import decimal_pb2  # type: ignore
import proto  # type: ignore

__protobuf__ = proto.module(
    package="google.cloud.channel.v1",
    manifest={
        "RebillingBasis",
        "CustomerRepricingConfig",
        "ChannelPartnerRepricingConfig",
        "RepricingConfig",
        "RepricingAdjustment",
        "PercentageAdjustment",
    },
)


class RebillingBasis(proto.Enum):
    r"""Specifies the different costs that the modified bill can be
    based on.
    """
    REBILLING_BASIS_UNSPECIFIED = 0
    COST_AT_LIST = 1
    DIRECT_CUSTOMER_COST = 2


class CustomerRepricingConfig(proto.Message):
    r"""Configuration for how a reseller will reprice a Customer.

    Attributes:
        name (str):
            Output only. Resource name of the CustomerRepricingConfig.
            Format:
            accounts/{account_id}/customers/{customer_id}/customerRepricingConfigs/{id}.
        repricing_config (google.cloud.channel_v1.types.RepricingConfig):
            Required. The configuration for bill
            modifications made by a reseller before sending
            it to customers.
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. Timestamp of an update to the repricing rule.
            If ``update_time`` is after
            [RepricingConfig.effective_invoice_month][google.cloud.channel.v1.RepricingConfig.effective_invoice_month]
            then it indicates this was set mid-month.
    """

    name = proto.Field(
        proto.STRING,
        number=1,
    )
    repricing_config = proto.Field(
        proto.MESSAGE,
        number=2,
        message="RepricingConfig",
    )
    update_time = proto.Field(
        proto.MESSAGE,
        number=3,
        message=timestamp_pb2.Timestamp,
    )


class ChannelPartnerRepricingConfig(proto.Message):
    r"""Configuration for how a distributor will rebill a channel
    partner (also known as a distributor-authorized reseller).

    Attributes:
        name (str):
            Output only. Resource name of the
            ChannelPartnerRepricingConfig. Format:
            accounts/{account_id}/channelPartnerLinks/{channel_partner_id}/channelPartnerRepricingConfigs/{id}.
        repricing_config (google.cloud.channel_v1.types.RepricingConfig):
            Required. The configuration for bill
            modifications made by a reseller before sending
            it to ChannelPartner.
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. Timestamp of an update to the repricing rule.
            If ``update_time`` is after
            [RepricingConfig.effective_invoice_month][google.cloud.channel.v1.RepricingConfig.effective_invoice_month]
            then it indicates this was set mid-month.
    """

    name = proto.Field(
        proto.STRING,
        number=1,
    )
    repricing_config = proto.Field(
        proto.MESSAGE,
        number=2,
        message="RepricingConfig",
    )
    update_time = proto.Field(
        proto.MESSAGE,
        number=3,
        message=timestamp_pb2.Timestamp,
    )


class RepricingConfig(proto.Message):
    r"""Configuration for repricing a Google bill over a period of
    time.

    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        entitlement_granularity (google.cloud.channel_v1.types.RepricingConfig.EntitlementGranularity):
            Applies the repricing configuration at the
            entitlement level. This is the only supported
            value for CustomerRepricingConfig.

            This field is a member of `oneof`_ ``granularity``.
        channel_partner_granularity (google.cloud.channel_v1.types.RepricingConfig.ChannelPartnerGranularity):
            Applies the repricing configuration at the
            channel partner level. This is the only
            supported value for
            ChannelPartnerRepricingConfig.

            This field is a member of `oneof`_ ``granularity``.
        effective_invoice_month (google.type.date_pb2.Date):
            Required. The YearMonth when these
            adjustments activate. The Day field needs to be
            "0" since we only accept YearMonth repricing
            boundaries.
        adjustment (google.cloud.channel_v1.types.RepricingAdjustment):
            Required. Information about the adjustment.
        rebilling_basis (google.cloud.channel_v1.types.RebillingBasis):
            Required. The
            [RebillingBasis][google.cloud.channel.v1.RebillingBasis] to
            use for this bill. Specifies the relative cost based on
            repricing costs you will apply.
    """

    class EntitlementGranularity(proto.Message):
        r"""Applies the repricing configuration at the entitlement level.

        Attributes:
            entitlement (str):
                Resource name of the entitlement. Format:
                accounts/{account_id}/customers/{customer_id}/entitlements/{entitlement_id}
        """

        entitlement = proto.Field(
            proto.STRING,
            number=1,
        )

    class ChannelPartnerGranularity(proto.Message):
        r"""Applies the repricing configuration at the channel partner
        level. The channel partner value is derived from the resource
        name. Takes an empty json object.

        """

    entitlement_granularity = proto.Field(
        proto.MESSAGE,
        number=4,
        oneof="granularity",
        message=EntitlementGranularity,
    )
    channel_partner_granularity = proto.Field(
        proto.MESSAGE,
        number=5,
        oneof="granularity",
        message=ChannelPartnerGranularity,
    )
    effective_invoice_month = proto.Field(
        proto.MESSAGE,
        number=1,
        message=date_pb2.Date,
    )
    adjustment = proto.Field(
        proto.MESSAGE,
        number=2,
        message="RepricingAdjustment",
    )
    rebilling_basis = proto.Field(
        proto.ENUM,
        number=3,
        enum="RebillingBasis",
    )


class RepricingAdjustment(proto.Message):
    r"""A type that represents the various adjustments you can apply
    to a bill.


    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        percentage_adjustment (google.cloud.channel_v1.types.PercentageAdjustment):
            Flat markup or markdown on an entire bill.

            This field is a member of `oneof`_ ``adjustment``.
    """

    percentage_adjustment = proto.Field(
        proto.MESSAGE,
        number=2,
        oneof="adjustment",
        message="PercentageAdjustment",
    )


class PercentageAdjustment(proto.Message):
    r"""An adjustment that applies a flat markup or markdown to an
    entire bill.

    Attributes:
        percentage (google.type.decimal_pb2.Decimal):
            The percentage of the bill to adjust.
            For example:
            Mark down by 1% => "-1.00"
            Mark up by 1%   => "1.00"
            Pass-Through    => "0.00".
    """

    percentage = proto.Field(
        proto.MESSAGE,
        number=2,
        message=decimal_pb2.Decimal,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
