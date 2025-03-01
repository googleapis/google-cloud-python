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

from google.protobuf import timestamp_pb2  # type: ignore
from google.protobuf import wrappers_pb2  # type: ignore
from google.type import latlng_pb2  # type: ignore


__protobuf__ = proto.module(
    package='maps.fleetengine.delivery.v1',
    manifest={
        'DeliveryVehicleLocationSensor',
        'DeliveryVehicleNavigationStatus',
        'DeliveryVehicleAttribute',
        'DeliveryVehicleLocation',
        'TimeWindow',
        'TaskAttribute',
    },
)


class DeliveryVehicleLocationSensor(proto.Enum):
    r"""The sensor or methodology used to determine the location.

    Values:
        UNKNOWN_SENSOR (0):
            The sensor is unspecified or unknown.
        GPS (1):
            GPS or Assisted GPS.
        NETWORK (2):
            Assisted GPS, cell tower ID, or WiFi access
            point.
        PASSIVE (3):
            Cell tower ID or WiFi access point.
        ROAD_SNAPPED_LOCATION_PROVIDER (4):
            A location determined by the mobile device to
            be the most likely road position.
        CUSTOMER_SUPPLIED_LOCATION (5):
            A customer-supplied location from an independent source.
            Typically, this value is used for a location provided from
            sources other than the mobile device running Driver SDK. If
            the original source is described by one of the other enum
            values, use that value. Locations marked
            CUSTOMER_SUPPLIED_LOCATION are typically provided via a
            DeliveryVehicle's
            ``last_location.supplemental_location_sensor``.
        FLEET_ENGINE_LOCATION (6):
            A location calculated by Fleet Engine based
            on the signals available to it. Output only.
            This value will be rejected if it is received in
            a request.
        FUSED_LOCATION_PROVIDER (100):
            Android's Fused Location Provider.
        CORE_LOCATION (200):
            The location provider on Apple operating
            systems.
    """
    UNKNOWN_SENSOR = 0
    GPS = 1
    NETWORK = 2
    PASSIVE = 3
    ROAD_SNAPPED_LOCATION_PROVIDER = 4
    CUSTOMER_SUPPLIED_LOCATION = 5
    FLEET_ENGINE_LOCATION = 6
    FUSED_LOCATION_PROVIDER = 100
    CORE_LOCATION = 200


class DeliveryVehicleNavigationStatus(proto.Enum):
    r"""The vehicle's navigation status.

    Values:
        UNKNOWN_NAVIGATION_STATUS (0):
            Unspecified navigation status.
        NO_GUIDANCE (1):
            The Driver app's navigation is in ``FREE_NAV`` mode.
        ENROUTE_TO_DESTINATION (2):
            Turn-by-turn navigation is available and the Driver app
            navigation has entered ``GUIDED_NAV`` mode.
        OFF_ROUTE (3):
            The vehicle has gone off the suggested route.
        ARRIVED_AT_DESTINATION (4):
            The vehicle is within approximately 50m of
            the destination.
    """
    UNKNOWN_NAVIGATION_STATUS = 0
    NO_GUIDANCE = 1
    ENROUTE_TO_DESTINATION = 2
    OFF_ROUTE = 3
    ARRIVED_AT_DESTINATION = 4


class DeliveryVehicleAttribute(proto.Message):
    r"""Describes a vehicle attribute as a key-value pair. The
    "key:value" string length cannot exceed 256 characters.

    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        key (str):
            The attribute's key.
        value (str):
            The attribute's value.
        string_value (str):
            String typed attribute value.

            Note: This is identical to the ``value`` field which will
            eventually be deprecated. For create or update methods,
            either field can be used, but it's strongly recommended to
            use ``string_value``. If both ``string_value`` and ``value``
            are set, they must be identical or an error will be thrown.
            Both fields are populated in responses.

            This field is a member of `oneof`_ ``delivery_vehicle_attribute_value``.
        bool_value (bool):
            Boolean typed attribute value.

            This field is a member of `oneof`_ ``delivery_vehicle_attribute_value``.
        number_value (float):
            Double typed attribute value.

            This field is a member of `oneof`_ ``delivery_vehicle_attribute_value``.
    """

    key: str = proto.Field(
        proto.STRING,
        number=1,
    )
    value: str = proto.Field(
        proto.STRING,
        number=2,
    )
    string_value: str = proto.Field(
        proto.STRING,
        number=3,
        oneof='delivery_vehicle_attribute_value',
    )
    bool_value: bool = proto.Field(
        proto.BOOL,
        number=4,
        oneof='delivery_vehicle_attribute_value',
    )
    number_value: float = proto.Field(
        proto.DOUBLE,
        number=5,
        oneof='delivery_vehicle_attribute_value',
    )


class DeliveryVehicleLocation(proto.Message):
    r"""The location, speed, and heading of a vehicle at a point in
    time.

    Attributes:
        location (google.type.latlng_pb2.LatLng):
            The location of the vehicle. When it is sent to Fleet
            Engine, the vehicle's location is a GPS location. When you
            receive it in a response, the vehicle's location can be
            either a GPS location, a supplemental location, or some
            other estimated location. The source is specified in
            ``location_sensor``.
        horizontal_accuracy (google.protobuf.wrappers_pb2.DoubleValue):
            Deprecated: Use ``latlng_accuracy`` instead.
        latlng_accuracy (google.protobuf.wrappers_pb2.DoubleValue):
            Accuracy of ``location`` in meters as a radius.
        heading (google.protobuf.wrappers_pb2.Int32Value):
            Direction the vehicle is moving in degrees. 0 represents
            North. The valid range is [0,360).
        bearing_accuracy (google.protobuf.wrappers_pb2.DoubleValue):
            Deprecated: Use ``heading_accuracy`` instead.
        heading_accuracy (google.protobuf.wrappers_pb2.DoubleValue):
            Accuracy of ``heading`` in degrees.
        altitude (google.protobuf.wrappers_pb2.DoubleValue):
            Altitude in meters above WGS84.
        vertical_accuracy (google.protobuf.wrappers_pb2.DoubleValue):
            Deprecated: Use ``altitude_accuracy`` instead.
        altitude_accuracy (google.protobuf.wrappers_pb2.DoubleValue):
            Accuracy of ``altitude`` in meters.
        speed_kmph (google.protobuf.wrappers_pb2.Int32Value):
            Speed of the vehicle in kilometers per hour. Deprecated: Use
            ``speed`` instead.
        speed (google.protobuf.wrappers_pb2.DoubleValue):
            Speed of the vehicle in meters/second
        speed_accuracy (google.protobuf.wrappers_pb2.DoubleValue):
            Accuracy of ``speed`` in meters/second.
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            The time when ``location`` was reported by the sensor
            according to the sensor's clock.
        server_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time when the server
            received the location information.
        location_sensor (google.maps.fleetengine_delivery_v1.types.DeliveryVehicleLocationSensor):
            Provider of location data (for example, ``GPS``).
        is_road_snapped (google.protobuf.wrappers_pb2.BoolValue):
            Whether ``location`` is snapped to a road.
        is_gps_sensor_enabled (google.protobuf.wrappers_pb2.BoolValue):
            Input only. Indicates whether the GPS sensor
            is enabled on the mobile device.
        time_since_update (google.protobuf.wrappers_pb2.Int32Value):
            Input only. Time (in seconds) since this
            location was first sent to the server. This will
            be zero for the first update. If the time is
            unknown (for example, when the app restarts),
            this value resets to zero.
        num_stale_updates (google.protobuf.wrappers_pb2.Int32Value):
            Input only. Deprecated: Other signals are now
            used to determine if a location is stale.
        raw_location (google.type.latlng_pb2.LatLng):
            Raw vehicle location (unprocessed by
            road-snapper).
        raw_location_time (google.protobuf.timestamp_pb2.Timestamp):
            Timestamp associated with the raw location.
        raw_location_sensor (google.maps.fleetengine_delivery_v1.types.DeliveryVehicleLocationSensor):
            Source of the raw location. Defaults to ``GPS``.
        raw_location_accuracy (google.protobuf.wrappers_pb2.DoubleValue):
            Accuracy of ``raw_location`` as a radius, in meters.
        supplemental_location (google.type.latlng_pb2.LatLng):
            Supplemental location provided by the
            integrating app.
        supplemental_location_time (google.protobuf.timestamp_pb2.Timestamp):
            Timestamp associated with the supplemental
            location.
        supplemental_location_sensor (google.maps.fleetengine_delivery_v1.types.DeliveryVehicleLocationSensor):
            Source of the supplemental location. Defaults to
            ``CUSTOMER_SUPPLIED_LOCATION``.
        supplemental_location_accuracy (google.protobuf.wrappers_pb2.DoubleValue):
            Accuracy of ``supplemental_location`` as a radius, in
            meters.
        road_snapped (bool):
            Deprecated: Use ``is_road_snapped`` instead.
    """

    location: latlng_pb2.LatLng = proto.Field(
        proto.MESSAGE,
        number=1,
        message=latlng_pb2.LatLng,
    )
    horizontal_accuracy: wrappers_pb2.DoubleValue = proto.Field(
        proto.MESSAGE,
        number=8,
        message=wrappers_pb2.DoubleValue,
    )
    latlng_accuracy: wrappers_pb2.DoubleValue = proto.Field(
        proto.MESSAGE,
        number=22,
        message=wrappers_pb2.DoubleValue,
    )
    heading: wrappers_pb2.Int32Value = proto.Field(
        proto.MESSAGE,
        number=2,
        message=wrappers_pb2.Int32Value,
    )
    bearing_accuracy: wrappers_pb2.DoubleValue = proto.Field(
        proto.MESSAGE,
        number=10,
        message=wrappers_pb2.DoubleValue,
    )
    heading_accuracy: wrappers_pb2.DoubleValue = proto.Field(
        proto.MESSAGE,
        number=23,
        message=wrappers_pb2.DoubleValue,
    )
    altitude: wrappers_pb2.DoubleValue = proto.Field(
        proto.MESSAGE,
        number=5,
        message=wrappers_pb2.DoubleValue,
    )
    vertical_accuracy: wrappers_pb2.DoubleValue = proto.Field(
        proto.MESSAGE,
        number=9,
        message=wrappers_pb2.DoubleValue,
    )
    altitude_accuracy: wrappers_pb2.DoubleValue = proto.Field(
        proto.MESSAGE,
        number=24,
        message=wrappers_pb2.DoubleValue,
    )
    speed_kmph: wrappers_pb2.Int32Value = proto.Field(
        proto.MESSAGE,
        number=3,
        message=wrappers_pb2.Int32Value,
    )
    speed: wrappers_pb2.DoubleValue = proto.Field(
        proto.MESSAGE,
        number=6,
        message=wrappers_pb2.DoubleValue,
    )
    speed_accuracy: wrappers_pb2.DoubleValue = proto.Field(
        proto.MESSAGE,
        number=7,
        message=wrappers_pb2.DoubleValue,
    )
    update_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=4,
        message=timestamp_pb2.Timestamp,
    )
    server_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=13,
        message=timestamp_pb2.Timestamp,
    )
    location_sensor: 'DeliveryVehicleLocationSensor' = proto.Field(
        proto.ENUM,
        number=11,
        enum='DeliveryVehicleLocationSensor',
    )
    is_road_snapped: wrappers_pb2.BoolValue = proto.Field(
        proto.MESSAGE,
        number=27,
        message=wrappers_pb2.BoolValue,
    )
    is_gps_sensor_enabled: wrappers_pb2.BoolValue = proto.Field(
        proto.MESSAGE,
        number=12,
        message=wrappers_pb2.BoolValue,
    )
    time_since_update: wrappers_pb2.Int32Value = proto.Field(
        proto.MESSAGE,
        number=14,
        message=wrappers_pb2.Int32Value,
    )
    num_stale_updates: wrappers_pb2.Int32Value = proto.Field(
        proto.MESSAGE,
        number=15,
        message=wrappers_pb2.Int32Value,
    )
    raw_location: latlng_pb2.LatLng = proto.Field(
        proto.MESSAGE,
        number=16,
        message=latlng_pb2.LatLng,
    )
    raw_location_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=17,
        message=timestamp_pb2.Timestamp,
    )
    raw_location_sensor: 'DeliveryVehicleLocationSensor' = proto.Field(
        proto.ENUM,
        number=28,
        enum='DeliveryVehicleLocationSensor',
    )
    raw_location_accuracy: wrappers_pb2.DoubleValue = proto.Field(
        proto.MESSAGE,
        number=25,
        message=wrappers_pb2.DoubleValue,
    )
    supplemental_location: latlng_pb2.LatLng = proto.Field(
        proto.MESSAGE,
        number=18,
        message=latlng_pb2.LatLng,
    )
    supplemental_location_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=19,
        message=timestamp_pb2.Timestamp,
    )
    supplemental_location_sensor: 'DeliveryVehicleLocationSensor' = proto.Field(
        proto.ENUM,
        number=20,
        enum='DeliveryVehicleLocationSensor',
    )
    supplemental_location_accuracy: wrappers_pb2.DoubleValue = proto.Field(
        proto.MESSAGE,
        number=21,
        message=wrappers_pb2.DoubleValue,
    )
    road_snapped: bool = proto.Field(
        proto.BOOL,
        number=26,
    )


class TimeWindow(proto.Message):
    r"""A time range.

    Attributes:
        start_time (google.protobuf.timestamp_pb2.Timestamp):
            Required. The start time of the time window
            (inclusive).
        end_time (google.protobuf.timestamp_pb2.Timestamp):
            Required. The end time of the time window
            (inclusive).
    """

    start_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=1,
        message=timestamp_pb2.Timestamp,
    )
    end_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=2,
        message=timestamp_pb2.Timestamp,
    )


class TaskAttribute(proto.Message):
    r"""Describes a task attribute as a key-value pair. The
    "key:value" string length cannot exceed 256 characters.

    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        key (str):
            The attribute's key. Keys may not contain the
            colon character (:).
        string_value (str):
            String typed attribute value.

            This field is a member of `oneof`_ ``task_attribute_value``.
        bool_value (bool):
            Boolean typed attribute value.

            This field is a member of `oneof`_ ``task_attribute_value``.
        number_value (float):
            Double typed attribute value.

            This field is a member of `oneof`_ ``task_attribute_value``.
    """

    key: str = proto.Field(
        proto.STRING,
        number=1,
    )
    string_value: str = proto.Field(
        proto.STRING,
        number=2,
        oneof='task_attribute_value',
    )
    bool_value: bool = proto.Field(
        proto.BOOL,
        number=3,
        oneof='task_attribute_value',
    )
    number_value: float = proto.Field(
        proto.DOUBLE,
        number=4,
        oneof='task_attribute_value',
    )


__all__ = tuple(sorted(__protobuf__.manifest))
