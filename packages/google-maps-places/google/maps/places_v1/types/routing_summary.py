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

from google.protobuf import duration_pb2  # type: ignore
import proto  # type: ignore

__protobuf__ = proto.module(
    package="google.maps.places.v1",
    manifest={
        "RoutingSummary",
    },
)


class RoutingSummary(proto.Message):
    r"""The duration and distance from the routing origin to a place in the
    response, and a second leg from that place to the destination, if
    requested. Note: Adding ``routingSummaries`` in the field mask
    without also including either the ``routingParameters.origin``
    parameter or the
    ``searchAlongRouteParameters.polyline.encodedPolyline`` parameter in
    the request causes an error.

    Attributes:
        legs (MutableSequence[google.maps.places_v1.types.RoutingSummary.Leg]):
            The legs of the trip.

            When you calculate travel duration and distance from a set
            origin, ``legs`` contains a single leg containing the
            duration and distance from the origin to the destination.
            When you do a search along route, ``legs`` contains two
            legs: one from the origin to place, and one from the place
            to the destination.
    """

    class Leg(proto.Message):
        r"""A leg is a single portion of a journey from one location to
        another.

        Attributes:
            duration (google.protobuf.duration_pb2.Duration):
                The time it takes to complete this leg of the
                trip.
            distance_meters (int):
                The distance of this leg of the trip.
        """

        duration: duration_pb2.Duration = proto.Field(
            proto.MESSAGE,
            number=1,
            message=duration_pb2.Duration,
        )
        distance_meters: int = proto.Field(
            proto.INT32,
            number=2,
        )

    legs: MutableSequence[Leg] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message=Leg,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
