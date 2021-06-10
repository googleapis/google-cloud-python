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


__protobuf__ = proto.module(
    package="google.cloud.channel.v1",
    manifest={"CustomerEvent", "EntitlementEvent", "SubscriberEvent",},
)


class CustomerEvent(proto.Message):
    r"""Represents Pub/Sub message content describing customer
    update.

    Attributes:
        customer (str):
            Resource name of the customer. Format:
            accounts/{account_id}/customers/{customer_id}
        event_type (google.cloud.channel_v1.types.CustomerEvent.Type):
            Type of event which happened on the customer.
    """

    class Type(proto.Enum):
        r"""Type of customer event."""
        TYPE_UNSPECIFIED = 0
        PRIMARY_DOMAIN_CHANGED = 1
        PRIMARY_DOMAIN_VERIFIED = 2

    customer = proto.Field(proto.STRING, number=1,)
    event_type = proto.Field(proto.ENUM, number=2, enum=Type,)


class EntitlementEvent(proto.Message):
    r"""Represents Pub/Sub message content describing entitlement
    update.

    Attributes:
        entitlement (str):
            Resource name of an entitlement of the form:
            accounts/{account_id}/customers/{customer_id}/entitlements/{entitlement_id}
        event_type (google.cloud.channel_v1.types.EntitlementEvent.Type):
            Type of event which happened on the
            entitlement.
    """

    class Type(proto.Enum):
        r"""Type of entitlement event."""
        TYPE_UNSPECIFIED = 0
        CREATED = 1
        PRICE_PLAN_SWITCHED = 3
        COMMITMENT_CHANGED = 4
        RENEWED = 5
        SUSPENDED = 6
        ACTIVATED = 7
        CANCELLED = 8
        SKU_CHANGED = 9
        RENEWAL_SETTING_CHANGED = 10
        PAID_SERVICE_STARTED = 11
        LICENSE_ASSIGNMENT_CHANGED = 12
        LICENSE_CAP_CHANGED = 13

    entitlement = proto.Field(proto.STRING, number=1,)
    event_type = proto.Field(proto.ENUM, number=2, enum=Type,)


class SubscriberEvent(proto.Message):
    r"""Represents information which resellers will get as part of
    notification from Cloud Pub/Sub.

    Attributes:
        customer_event (google.cloud.channel_v1.types.CustomerEvent):
            Customer event send as part of Pub/Sub event
            to partners.
        entitlement_event (google.cloud.channel_v1.types.EntitlementEvent):
            Entitlement event send as part of Pub/Sub
            event to partners.
    """

    customer_event = proto.Field(
        proto.MESSAGE, number=1, oneof="event", message="CustomerEvent",
    )
    entitlement_event = proto.Field(
        proto.MESSAGE, number=2, oneof="event", message="EntitlementEvent",
    )


__all__ = tuple(sorted(__protobuf__.manifest))
