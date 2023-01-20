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
from typing import MutableMapping, MutableSequence

import google.geo.type.types
from google.protobuf import duration_pb2  # type: ignore
import proto  # type: ignore

from google.maps.routing_v2.types import (
    navigation_instruction as gmr_navigation_instruction,
)
from google.maps.routing_v2.types import location
from google.maps.routing_v2.types import polyline as gmr_polyline
from google.maps.routing_v2.types import route_label, speed_reading_interval
from google.maps.routing_v2.types import toll_info as gmr_toll_info

__protobuf__ = proto.module(
    package="google.maps.routing.v2",
    manifest={
        "Route",
        "RouteTravelAdvisory",
        "RouteLegTravelAdvisory",
        "RouteLegStepTravelAdvisory",
        "RouteLeg",
        "RouteLegStep",
    },
)


class Route(proto.Message):
    r"""Encapsulates a route, which consists of a series of connected
    road segments that join beginning, ending, and intermediate
    waypoints.

    Attributes:
        route_labels (MutableSequence[google.maps.routing_v2.types.RouteLabel]):
            Labels for the ``Route`` that are useful to identify
            specific properties of the route to compare against others.
        legs (MutableSequence[google.maps.routing_v2.types.RouteLeg]):
            A collection of legs (path segments between waypoints) that
            make-up the route. Each leg corresponds to the trip between
            two non-\ ``via`` Waypoints. For example, a route with no
            intermediate waypoints has only one leg. A route that
            includes one non-\ ``via`` intermediate waypoint has two
            legs. A route that includes one ``via`` intermediate
            waypoint has one leg. The order of the legs matches the
            order of Waypoints from ``origin`` to ``intermediates`` to
            ``destination``.
        distance_meters (int):
            The travel distance of the route, in meters.
        duration (google.protobuf.duration_pb2.Duration):
            The length of time needed to navigate the route. If you set
            the ``routing_preference`` to ``TRAFFIC_UNAWARE``, then this
            value is the same as ``static_duration``. If you set the
            ``routing_preference`` to either ``TRAFFIC_AWARE`` or
            ``TRAFFIC_AWARE_OPTIMAL``, then this value is calculated
            taking traffic conditions into account.
        static_duration (google.protobuf.duration_pb2.Duration):
            The duration of traveling through the route
            without taking traffic conditions into
            consideration.
        polyline (google.maps.routing_v2.types.Polyline):
            The overall route polyline. This polyline will be the
            combined polyline of all ``legs``.
        description (str):
            A description of the route.
        warnings (MutableSequence[str]):
            An array of warnings to show when displaying
            the route.
        viewport (google.geo.type.types.Viewport):
            The viewport bounding box of the polyline.
        travel_advisory (google.maps.routing_v2.types.RouteTravelAdvisory):
            Additional information about the route.
        route_token (str):
            Web-safe base64 encoded route token that can be passed to
            NavigationSDK, which allows the Navigation SDK to
            reconstruct the route during navigation, and in the event of
            rerouting honor the original intention when Routes
            ComputeRoutes is called. Customers should treat this token
            as an opaque blob. NOTE: ``Route.route_token`` is only
            available for requests that have set
            ``ComputeRoutesRequest.routing_preference`` to
            ``TRAFFIC_AWARE`` or ``TRAFFIC_AWARE_OPTIMAL``.
            ``Route.route_token`` is also not supported for requests
            that have Via waypoints.
    """

    route_labels: MutableSequence[route_label.RouteLabel] = proto.RepeatedField(
        proto.ENUM,
        number=13,
        enum=route_label.RouteLabel,
    )
    legs: MutableSequence["RouteLeg"] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="RouteLeg",
    )
    distance_meters: int = proto.Field(
        proto.INT32,
        number=2,
    )
    duration: duration_pb2.Duration = proto.Field(
        proto.MESSAGE,
        number=3,
        message=duration_pb2.Duration,
    )
    static_duration: duration_pb2.Duration = proto.Field(
        proto.MESSAGE,
        number=4,
        message=duration_pb2.Duration,
    )
    polyline: gmr_polyline.Polyline = proto.Field(
        proto.MESSAGE,
        number=5,
        message=gmr_polyline.Polyline,
    )
    description: str = proto.Field(
        proto.STRING,
        number=6,
    )
    warnings: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=7,
    )
    viewport: google.geo.type.types.Viewport = proto.Field(
        proto.MESSAGE,
        number=8,
        message=google.geo.type.types.Viewport,
    )
    travel_advisory: "RouteTravelAdvisory" = proto.Field(
        proto.MESSAGE,
        number=9,
        message="RouteTravelAdvisory",
    )
    route_token: str = proto.Field(
        proto.STRING,
        number=12,
    )


class RouteTravelAdvisory(proto.Message):
    r"""Encapsulates the additional information that the user should
    be informed about, such as possible traffic zone restriction
    etc.

    Attributes:
        toll_info (google.maps.routing_v2.types.TollInfo):
            Encapsulates information about tolls on the Route. This
            field is only populated if we expect there are tolls on the
            Route. If this field is set but the estimated_price subfield
            is not populated, we expect that road contains tolls but we
            do not know an estimated price. If this field is not set,
            then we expect there is no toll on the Route.
        speed_reading_intervals (MutableSequence[google.maps.routing_v2.types.SpeedReadingInterval]):
            Speed reading intervals detailing traffic density.
            Applicable in case of ``TRAFFIC_AWARE`` and
            ``TRAFFIC_AWARE_OPTIMAL`` routing preferences. The intervals
            cover the entire polyline of the route without overlap. The
            start point of a specified interval is the same as the end
            point of the preceding interval.

            Example:

            ::

                polyline: A ---- B ---- C ---- D ---- E ---- F ---- G
                speed_reading_intervals: [A,C), [C,D), [D,G).
        fuel_consumption_microliters (int):
            The fuel consumption prediction in
            microliters.
    """

    toll_info: gmr_toll_info.TollInfo = proto.Field(
        proto.MESSAGE,
        number=2,
        message=gmr_toll_info.TollInfo,
    )
    speed_reading_intervals: MutableSequence[
        speed_reading_interval.SpeedReadingInterval
    ] = proto.RepeatedField(
        proto.MESSAGE,
        number=3,
        message=speed_reading_interval.SpeedReadingInterval,
    )
    fuel_consumption_microliters: int = proto.Field(
        proto.INT64,
        number=5,
    )


class RouteLegTravelAdvisory(proto.Message):
    r"""Encapsulates the additional information that the user should
    be informed about, such as possible traffic zone restriction
    etc. on a route leg.

    Attributes:
        toll_info (google.maps.routing_v2.types.TollInfo):
            Encapsulates information about tolls on the specific
            RouteLeg. This field is only populated if we expect there
            are tolls on the RouteLeg. If this field is set but the
            estimated_price subfield is not populated, we expect that
            road contains tolls but we do not know an estimated price.
            If this field does not exist, then there is no toll on the
            RouteLeg.
        speed_reading_intervals (MutableSequence[google.maps.routing_v2.types.SpeedReadingInterval]):
            Speed reading intervals detailing traffic density.
            Applicable in case of ``TRAFFIC_AWARE`` and
            ``TRAFFIC_AWARE_OPTIMAL`` routing preferences. The intervals
            cover the entire polyline of the RouteLg without overlap.
            The start point of a specified interval is the same as the
            end point of the preceding interval.

            Example:

            ::

                polyline: A ---- B ---- C ---- D ---- E ---- F ---- G
                speed_reading_intervals: [A,C), [C,D), [D,G).
    """

    toll_info: gmr_toll_info.TollInfo = proto.Field(
        proto.MESSAGE,
        number=1,
        message=gmr_toll_info.TollInfo,
    )
    speed_reading_intervals: MutableSequence[
        speed_reading_interval.SpeedReadingInterval
    ] = proto.RepeatedField(
        proto.MESSAGE,
        number=2,
        message=speed_reading_interval.SpeedReadingInterval,
    )


class RouteLegStepTravelAdvisory(proto.Message):
    r"""Encapsulates the additional information that the user should
    be informed about, such as possible traffic zone restriction on
    a leg step.

    Attributes:
        speed_reading_intervals (MutableSequence[google.maps.routing_v2.types.SpeedReadingInterval]):
            Speed reading intervals detailing traffic density.
            Applicable in case of ``TRAFFIC_AWARE`` and
            ``TRAFFIC_AWARE_OPTIMAL`` routing preferences. The intervals
            cover the entire polyline of the RouteLegStep without
            overlap. The start point of a specified interval is the same
            as the end point of the preceding interval.

            Example:

            ::

                polyline: A ---- B ---- C ---- D ---- E ---- F ---- G
                speed_reading_intervals: [A,C), [C,D), [D,G).
    """

    speed_reading_intervals: MutableSequence[
        speed_reading_interval.SpeedReadingInterval
    ] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message=speed_reading_interval.SpeedReadingInterval,
    )


class RouteLeg(proto.Message):
    r"""Encapsulates a segment between non-\ ``via`` waypoints.

    Attributes:
        distance_meters (int):
            The travel distance of the route leg, in
            meters.
        duration (google.protobuf.duration_pb2.Duration):
            The length of time needed to navigate the leg. If the
            ``route_preference`` is set to ``TRAFFIC_UNAWARE``, then
            this value is the same as ``static_duration``. If the
            ``route_preference`` is either ``TRAFFIC_AWARE`` or
            ``TRAFFIC_AWARE_OPTIMAL``, then this value is calculated
            taking traffic conditions into account.
        static_duration (google.protobuf.duration_pb2.Duration):
            The duration of traveling through the leg,
            calculated without taking traffic conditions
            into consideration.
        polyline (google.maps.routing_v2.types.Polyline):
            The overall polyline for this leg. This includes that each
            ``step``'s polyline.
        start_location (google.maps.routing_v2.types.Location):
            The start location of this leg. This might be different from
            the provided ``origin``. For example, when the provided
            ``origin`` is not near a road, this is a point on the road.
        end_location (google.maps.routing_v2.types.Location):
            The end location of this leg. This might be different from
            the provided ``destination``. For example, when the provided
            ``destination`` is not near a road, this is a point on the
            road.
        steps (MutableSequence[google.maps.routing_v2.types.RouteLegStep]):
            An array of steps denoting segments within
            this leg. Each step represents one navigation
            instruction.
        travel_advisory (google.maps.routing_v2.types.RouteLegTravelAdvisory):
            Encapsulates the additional information that
            the user should be informed about, such as
            possible traffic zone restriction etc. on a
            route leg.
    """

    distance_meters: int = proto.Field(
        proto.INT32,
        number=1,
    )
    duration: duration_pb2.Duration = proto.Field(
        proto.MESSAGE,
        number=2,
        message=duration_pb2.Duration,
    )
    static_duration: duration_pb2.Duration = proto.Field(
        proto.MESSAGE,
        number=3,
        message=duration_pb2.Duration,
    )
    polyline: gmr_polyline.Polyline = proto.Field(
        proto.MESSAGE,
        number=4,
        message=gmr_polyline.Polyline,
    )
    start_location: location.Location = proto.Field(
        proto.MESSAGE,
        number=5,
        message=location.Location,
    )
    end_location: location.Location = proto.Field(
        proto.MESSAGE,
        number=6,
        message=location.Location,
    )
    steps: MutableSequence["RouteLegStep"] = proto.RepeatedField(
        proto.MESSAGE,
        number=7,
        message="RouteLegStep",
    )
    travel_advisory: "RouteLegTravelAdvisory" = proto.Field(
        proto.MESSAGE,
        number=8,
        message="RouteLegTravelAdvisory",
    )


class RouteLegStep(proto.Message):
    r"""Encapsulates a segment of a ``RouteLeg``. A step corresponds to a
    single navigation instruction. Route legs are made up of steps.

    Attributes:
        distance_meters (int):
            The travel distance of this step, in meters.
            In some circumstances, this field might not have
            a value.
        static_duration (google.protobuf.duration_pb2.Duration):
            The duration of travel through this step
            without taking traffic conditions into
            consideration. In some circumstances, this field
            might not have a value.
        polyline (google.maps.routing_v2.types.Polyline):
            The polyline associated with this step.
        start_location (google.maps.routing_v2.types.Location):
            The start location of this step.
        end_location (google.maps.routing_v2.types.Location):
            The end location of this step.
        navigation_instruction (google.maps.routing_v2.types.NavigationInstruction):
            Navigation instructions.
        travel_advisory (google.maps.routing_v2.types.RouteLegStepTravelAdvisory):
            Encapsulates the additional information that
            the user should be informed about, such as
            possible traffic zone restriction on a leg step.
    """

    distance_meters: int = proto.Field(
        proto.INT32,
        number=1,
    )
    static_duration: duration_pb2.Duration = proto.Field(
        proto.MESSAGE,
        number=2,
        message=duration_pb2.Duration,
    )
    polyline: gmr_polyline.Polyline = proto.Field(
        proto.MESSAGE,
        number=3,
        message=gmr_polyline.Polyline,
    )
    start_location: location.Location = proto.Field(
        proto.MESSAGE,
        number=4,
        message=location.Location,
    )
    end_location: location.Location = proto.Field(
        proto.MESSAGE,
        number=5,
        message=location.Location,
    )
    navigation_instruction: gmr_navigation_instruction.NavigationInstruction = (
        proto.Field(
            proto.MESSAGE,
            number=6,
            message=gmr_navigation_instruction.NavigationInstruction,
        )
    )
    travel_advisory: "RouteLegStepTravelAdvisory" = proto.Field(
        proto.MESSAGE,
        number=7,
        message="RouteLegStepTravelAdvisory",
    )


__all__ = tuple(sorted(__protobuf__.manifest))
