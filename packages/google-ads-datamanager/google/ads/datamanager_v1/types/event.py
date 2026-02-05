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

import google.protobuf.timestamp_pb2 as timestamp_pb2  # type: ignore
import proto  # type: ignore

from google.ads.datamanager_v1.types import user_properties as gad_user_properties
from google.ads.datamanager_v1.types import cart_data as gad_cart_data
from google.ads.datamanager_v1.types import consent as gad_consent
from google.ads.datamanager_v1.types import device_info, experimental_field
from google.ads.datamanager_v1.types import user_data as gad_user_data

__protobuf__ = proto.module(
    package="google.ads.datamanager.v1",
    manifest={
        "EventSource",
        "Event",
        "AdIdentifiers",
        "CustomVariable",
        "EventParameter",
    },
)


class EventSource(proto.Enum):
    r"""The source of the event.

    Values:
        EVENT_SOURCE_UNSPECIFIED (0):
            Unspecified EventSource. Should never be
            used.
        WEB (1):
            The event was generated from a web browser.
        APP (2):
            The event was generated from an app.
        IN_STORE (3):
            The event was generated from an in-store
            transaction.
        PHONE (4):
            The event was generated from a phone call.
        OTHER (5):
            The event was generated from other sources.
    """
    EVENT_SOURCE_UNSPECIFIED = 0
    WEB = 1
    APP = 2
    IN_STORE = 3
    PHONE = 4
    OTHER = 5


class Event(proto.Message):
    r"""An event representing a user interaction with an advertiser's
    website or app.

    Attributes:
        destination_references (MutableSequence[str]):
            Optional. Reference string used to determine the
            destination. If empty, the event will be sent to all
            [destinations][google.ads.datamanager.v1.IngestEventsRequest.destinations]
            in the request.
        transaction_id (str):
            Optional. The unique identifier for this
            event. Required for conversions using multiple
            data sources.
        event_timestamp (google.protobuf.timestamp_pb2.Timestamp):
            Required. The time the event occurred.
        last_updated_timestamp (google.protobuf.timestamp_pb2.Timestamp):
            Optional. The last time the event was
            updated.
        user_data (google.ads.datamanager_v1.types.UserData):
            Optional. Pieces of user provided data,
            representing the user the event is associated
            with.
        consent (google.ads.datamanager_v1.types.Consent):
            Optional. Information about whether the
            associated user has provided different types of
            consent.
        ad_identifiers (google.ads.datamanager_v1.types.AdIdentifiers):
            Optional. Identifiers and other information
            used to match the conversion event with other
            online activity (such as ad clicks).
        currency (str):
            Optional. The currency code associated with
            all monetary values within this event.
        conversion_value (float):
            Optional. The conversion value associated
            with the event, for value-based conversions.
        event_source (google.ads.datamanager_v1.types.EventSource):
            Optional. Signal for where the event happened
            (web, app, in-store, etc.).
        event_device_info (google.ads.datamanager_v1.types.DeviceInfo):
            Optional. Information gathered about the
            device being used (if any) when the event
            happened.
        cart_data (google.ads.datamanager_v1.types.CartData):
            Optional. Information about the transaction
            and items associated with the event.
        custom_variables (MutableSequence[google.ads.datamanager_v1.types.CustomVariable]):
            Optional. Additional key/value pair
            information to send to the conversion containers
            (conversion action or FL activity).
        experimental_fields (MutableSequence[google.ads.datamanager_v1.types.ExperimentalField]):
            Optional. A list of key/value pairs for
            experimental fields that may eventually be
            promoted to be part of the API.
        user_properties (google.ads.datamanager_v1.types.UserProperties):
            Optional. Advertiser-assessed information
            about the user at the time that the event
            happened.
        event_name (str):
            Optional. The name of the event. Required for
            GA4 events.
        client_id (str):
            Optional. A unique identifier for the user
            instance of a web client for this GA4 web
            stream.
        user_id (str):
            Optional. A unique identifier for a user, as
            defined by the advertiser.
        additional_event_parameters (MutableSequence[google.ads.datamanager_v1.types.EventParameter]):
            Optional. A bucket of any `event
            parameters <https://developers.google.com/analytics/devguides/collection/protocol/ga4/reference/events>`__
            to be included within the event that were not already
            specified using other structured fields.
    """

    destination_references: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=1,
    )
    transaction_id: str = proto.Field(
        proto.STRING,
        number=2,
    )
    event_timestamp: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=3,
        message=timestamp_pb2.Timestamp,
    )
    last_updated_timestamp: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=4,
        message=timestamp_pb2.Timestamp,
    )
    user_data: gad_user_data.UserData = proto.Field(
        proto.MESSAGE,
        number=5,
        message=gad_user_data.UserData,
    )
    consent: gad_consent.Consent = proto.Field(
        proto.MESSAGE,
        number=6,
        message=gad_consent.Consent,
    )
    ad_identifiers: "AdIdentifiers" = proto.Field(
        proto.MESSAGE,
        number=7,
        message="AdIdentifiers",
    )
    currency: str = proto.Field(
        proto.STRING,
        number=8,
    )
    conversion_value: float = proto.Field(
        proto.DOUBLE,
        number=9,
    )
    event_source: "EventSource" = proto.Field(
        proto.ENUM,
        number=10,
        enum="EventSource",
    )
    event_device_info: device_info.DeviceInfo = proto.Field(
        proto.MESSAGE,
        number=11,
        message=device_info.DeviceInfo,
    )
    cart_data: gad_cart_data.CartData = proto.Field(
        proto.MESSAGE,
        number=12,
        message=gad_cart_data.CartData,
    )
    custom_variables: MutableSequence["CustomVariable"] = proto.RepeatedField(
        proto.MESSAGE,
        number=13,
        message="CustomVariable",
    )
    experimental_fields: MutableSequence[
        experimental_field.ExperimentalField
    ] = proto.RepeatedField(
        proto.MESSAGE,
        number=14,
        message=experimental_field.ExperimentalField,
    )
    user_properties: gad_user_properties.UserProperties = proto.Field(
        proto.MESSAGE,
        number=15,
        message=gad_user_properties.UserProperties,
    )
    event_name: str = proto.Field(
        proto.STRING,
        number=16,
    )
    client_id: str = proto.Field(
        proto.STRING,
        number=17,
    )
    user_id: str = proto.Field(
        proto.STRING,
        number=18,
    )
    additional_event_parameters: MutableSequence[
        "EventParameter"
    ] = proto.RepeatedField(
        proto.MESSAGE,
        number=19,
        message="EventParameter",
    )


class AdIdentifiers(proto.Message):
    r"""Identifiers and other information used to match the
    conversion event with other online activity (such as ad clicks).

    Attributes:
        session_attributes (str):
            Optional. Session attributes for event
            attribution and modeling.
        gclid (str):
            Optional. The Google click ID (gclid)
            associated with this event.
        gbraid (str):
            Optional. The click identifier for clicks
            associated with app events and originating from
            iOS devices starting with iOS14.
        wbraid (str):
            Optional. The click identifier for clicks
            associated with web events and originating from
            iOS devices starting with iOS14.
        landing_page_device_info (google.ads.datamanager_v1.types.DeviceInfo):
            Optional. Information gathered about the
            device being used (if any) at the time of
            landing onto the advertiser’s site after
            interacting with the ad.
    """

    session_attributes: str = proto.Field(
        proto.STRING,
        number=1,
    )
    gclid: str = proto.Field(
        proto.STRING,
        number=2,
    )
    gbraid: str = proto.Field(
        proto.STRING,
        number=3,
    )
    wbraid: str = proto.Field(
        proto.STRING,
        number=4,
    )
    landing_page_device_info: device_info.DeviceInfo = proto.Field(
        proto.MESSAGE,
        number=5,
        message=device_info.DeviceInfo,
    )


class CustomVariable(proto.Message):
    r"""Custom variable for ads conversions.

    Attributes:
        variable (str):
            Optional. The name of the custom variable to
            set. If the variable is not found for the given
            destination, it will be ignored.
        value (str):
            Optional. The value to store for the custom
            variable.
        destination_references (MutableSequence[str]):
            Optional. Reference string used to determine which of the
            [Event.destination_references][google.ads.datamanager.v1.Event.destination_references]
            the custom variable should be sent to. If empty, the
            [Event.destination_references][google.ads.datamanager.v1.Event.destination_references]
            will be used.
    """

    variable: str = proto.Field(
        proto.STRING,
        number=1,
    )
    value: str = proto.Field(
        proto.STRING,
        number=2,
    )
    destination_references: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=3,
    )


class EventParameter(proto.Message):
    r"""Event parameter for GA4 events.

    Attributes:
        parameter_name (str):
            Required. The name of the parameter to use.
        value (str):
            Required. The string representation of the
            value of the parameter to set.
    """

    parameter_name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    value: str = proto.Field(
        proto.STRING,
        number=2,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
