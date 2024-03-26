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

from google.protobuf import timestamp_pb2  # type: ignore
import proto  # type: ignore

from google.ads.admanager_v1.types import placement_enums

__protobuf__ = proto.module(
    package="google.ads.admanager.v1",
    manifest={
        "Placement",
        "GetPlacementRequest",
        "ListPlacementsRequest",
        "ListPlacementsResponse",
    },
)


class Placement(proto.Message):
    r"""The ``Placement`` resource.

    Attributes:
        name (str):
            Identifier. The resource name of the ``Placement``. Format:
            ``networks/{network_code}/placements/{placement_id}``
        placement_id (int):
            Output only. ``Placement`` ID.
        display_name (str):
            Required. The display name of the placement.
            Its maximum length is 255 characters.
        description (str):
            Optional. A description of the Placement.
            This value is optional and its maximum length is
            65,535 characters.
        placement_code (str):
            Output only. A string used to uniquely
            identify the Placement for purposes of serving
            the ad. This attribute is read-only and is
            assigned by Google when a placement is created.
        status (google.ads.admanager_v1.types.PlacementStatusEnum.PlacementStatus):
            Output only. The status of the Placement.
            This attribute is read-only.
        targeted_ad_units (MutableSequence[str]):
            Optional. The resource names of AdUnits that constitute the
            Placement. Format:
            "networks/{network_code}/adUnits/{ad_unit_id}".
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The instant this Placement was
            last modified.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    placement_id: int = proto.Field(
        proto.INT64,
        number=2,
    )
    display_name: str = proto.Field(
        proto.STRING,
        number=3,
    )
    description: str = proto.Field(
        proto.STRING,
        number=4,
    )
    placement_code: str = proto.Field(
        proto.STRING,
        number=5,
    )
    status: placement_enums.PlacementStatusEnum.PlacementStatus = proto.Field(
        proto.ENUM,
        number=6,
        enum=placement_enums.PlacementStatusEnum.PlacementStatus,
    )
    targeted_ad_units: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=7,
    )
    update_time: timestamp_pb2.Timestamp = proto.Field(
        proto.MESSAGE,
        number=9,
        message=timestamp_pb2.Timestamp,
    )


class GetPlacementRequest(proto.Message):
    r"""Request object for ``GetPlacement`` method.

    Attributes:
        name (str):
            Required. The resource name of the Placement. Format:
            ``networks/{network_code}/placements/{placement_id}``
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class ListPlacementsRequest(proto.Message):
    r"""Request object for ``ListPlacements`` method.

    Attributes:
        parent (str):
            Required. The parent, which owns this collection of
            Placements. Format: ``networks/{network_code}``
        page_size (int):
            Optional. The maximum number of ``Placements`` to return.
            The service may return fewer than this value. If
            unspecified, at most 50 ``Placements`` will be returned. The
            maximum value is 1000; values above 1000 will be coerced to
            1000.
        page_token (str):
            Optional. A page token, received from a previous
            ``ListPlacements`` call. Provide this to retrieve the
            subsequent page.

            When paginating, all other parameters provided to
            ``ListPlacements`` must match the call that provided the
            page token.
        filter (str):
            Optional. Expression to filter the response.
            See syntax details at
            https://developers.google.com/ad-manager/api/beta/filters
        order_by (str):
            Optional. Expression to specify sorting
            order. See syntax details at
            https://developers.google.com/ad-manager/api/beta/filters#order
        skip (int):
            Optional. Number of individual resources to
            skip while paginating.
    """

    parent: str = proto.Field(
        proto.STRING,
        number=1,
    )
    page_size: int = proto.Field(
        proto.INT32,
        number=2,
    )
    page_token: str = proto.Field(
        proto.STRING,
        number=3,
    )
    filter: str = proto.Field(
        proto.STRING,
        number=4,
    )
    order_by: str = proto.Field(
        proto.STRING,
        number=5,
    )
    skip: int = proto.Field(
        proto.INT32,
        number=6,
    )


class ListPlacementsResponse(proto.Message):
    r"""Response object for ``ListPlacementsRequest`` containing matching
    ``Placement`` objects.

    Attributes:
        placements (MutableSequence[google.ads.admanager_v1.types.Placement]):
            The ``Placement`` objects from the specified network.
        next_page_token (str):
            A token, which can be sent as ``page_token`` to retrieve the
            next page. If this field is omitted, there are no subsequent
            pages.
        total_size (int):
            Total number of ``Placement`` objects. If a filter was
            included in the request, this reflects the total number
            after the filtering is applied.

            ``total_size`` will not be calculated in the response unless
            it has been included in a response field mask. The response
            field mask can be provided to the method by using the URL
            parameter ``$fields`` or ``fields``, or by using the
            HTTP/gRPC header ``X-Goog-FieldMask``.

            For more information, see
            https://developers.google.com/ad-manager/api/beta/field-masks
    """

    @property
    def raw_page(self):
        return self

    placements: MutableSequence["Placement"] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="Placement",
    )
    next_page_token: str = proto.Field(
        proto.STRING,
        number=2,
    )
    total_size: int = proto.Field(
        proto.INT32,
        number=3,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
