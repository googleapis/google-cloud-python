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
    package="google.maps.routing.v2",
    manifest={
        "PolylineDetails",
    },
)


class PolylineDetails(proto.Message):
    r"""Details corresponding to a given index or contiguous segment of a
    polyline. Given a polyline with points P_0, P_1, ... , P_N
    (zero-based index), the ``PolylineDetails`` defines an interval and
    associated metadata.

    Attributes:
        flyover_info (MutableSequence[google.maps.routing_v2.types.PolylineDetails.FlyoverInfo]):
            Flyover details along the polyline.
        narrow_road_info (MutableSequence[google.maps.routing_v2.types.PolylineDetails.NarrowRoadInfo]):
            Narrow road details along the polyline.
    """

    class RoadFeatureState(proto.Enum):
        r"""Encapsulates the states of road features along a stretch of
        polyline.

        Values:
            ROAD_FEATURE_STATE_UNSPECIFIED (0):
                The road feature's state was not computed
                (default value).
            EXISTS (1):
                The road feature exists.
            DOES_NOT_EXIST (2):
                The road feature does not exist.
        """
        ROAD_FEATURE_STATE_UNSPECIFIED = 0
        EXISTS = 1
        DOES_NOT_EXIST = 2

    class PolylinePointIndex(proto.Message):
        r"""Encapsulates the start and end indexes for a polyline detail. For
        instances where the data corresponds to a single point,
        ``start_index`` and ``end_index`` will be equal.


        .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

        Attributes:
            start_index (int):
                The start index of this detail in the
                polyline.

                This field is a member of `oneof`_ ``_start_index``.
            end_index (int):
                The end index of this detail in the polyline.

                This field is a member of `oneof`_ ``_end_index``.
        """

        start_index: int = proto.Field(
            proto.INT32,
            number=1,
            optional=True,
        )
        end_index: int = proto.Field(
            proto.INT32,
            number=2,
            optional=True,
        )

    class FlyoverInfo(proto.Message):
        r"""Encapsulates information about flyovers along the polyline.

        Attributes:
            flyover_presence (google.maps.routing_v2.types.PolylineDetails.RoadFeatureState):
                Output only. Denotes whether a flyover exists
                for a given stretch of the polyline.
            polyline_point_index (google.maps.routing_v2.types.PolylineDetails.PolylinePointIndex):
                The location of flyover related information
                along the polyline.
        """

        flyover_presence: "PolylineDetails.RoadFeatureState" = proto.Field(
            proto.ENUM,
            number=1,
            enum="PolylineDetails.RoadFeatureState",
        )
        polyline_point_index: "PolylineDetails.PolylinePointIndex" = proto.Field(
            proto.MESSAGE,
            number=2,
            message="PolylineDetails.PolylinePointIndex",
        )

    class NarrowRoadInfo(proto.Message):
        r"""Encapsulates information about narrow roads along the
        polyline.

        Attributes:
            narrow_road_presence (google.maps.routing_v2.types.PolylineDetails.RoadFeatureState):
                Output only. Denotes whether a narrow road
                exists for a given stretch of the polyline.
            polyline_point_index (google.maps.routing_v2.types.PolylineDetails.PolylinePointIndex):
                The location of narrow road related
                information along the polyline.
        """

        narrow_road_presence: "PolylineDetails.RoadFeatureState" = proto.Field(
            proto.ENUM,
            number=1,
            enum="PolylineDetails.RoadFeatureState",
        )
        polyline_point_index: "PolylineDetails.PolylinePointIndex" = proto.Field(
            proto.MESSAGE,
            number=2,
            message="PolylineDetails.PolylinePointIndex",
        )

    flyover_info: MutableSequence[FlyoverInfo] = proto.RepeatedField(
        proto.MESSAGE,
        number=12,
        message=FlyoverInfo,
    )
    narrow_road_info: MutableSequence[NarrowRoadInfo] = proto.RepeatedField(
        proto.MESSAGE,
        number=13,
        message=NarrowRoadInfo,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
