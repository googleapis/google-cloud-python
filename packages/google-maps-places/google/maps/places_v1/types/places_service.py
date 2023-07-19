# -*- coding: utf-8 -*-
# Copyright 2023 Google LLC
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

from google.geo.type.types import viewport
import proto  # type: ignore

from google.maps.places_v1.types import geometry, place

__protobuf__ = proto.module(
    package="google.maps.places.v1",
    manifest={
        "Int32Range",
        "SearchTextRequest",
        "SearchTextResponse",
    },
)


class Int32Range(proto.Message):
    r"""int 32 range. Both min and max are optional. If only min is
    set, then the range only has a lower bound. If only max is set,
    then range only has an upper bound. At least one of min and max
    must be set. Values are inclusive.


    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        min_ (int):
            Lower bound. If unset, behavior is documented
            on the range field.

            This field is a member of `oneof`_ ``_min``.
        max_ (int):
            Upper bound. If unset, behavior is documented
            on the range field.

            This field is a member of `oneof`_ ``_max``.
    """

    min_: int = proto.Field(
        proto.INT32,
        number=1,
        optional=True,
    )
    max_: int = proto.Field(
        proto.INT32,
        number=2,
        optional=True,
    )


class SearchTextRequest(proto.Message):
    r"""Request data structure for SearchText.

    Attributes:
        text_query (str):
            Required. The text query for textual search.
        language_code (str):
            Place details will be displayed with the
            preferred language if available. If the language
            code is unspecified or unrecognized, place
            details of any language may be returned, with a
            preference for English if such details exist.

            Current list of supported languages:

            https://developers.google.com/maps/faq#languagesupport.
        region_code (str):
            The Unicode country/region code (CLDR) of the location where
            the request is coming from. It is used to display the place
            details, like region-specific place name, if available.

            For more information, see
            http://www.unicode.org/reports/tr35/#unicode_region_subtag.

            Note that 3-digit region codes are not currently supported.
        rank_preference (google.maps.places_v1.types.SearchTextRequest.RankPreference):
            How results will be ranked in the response.
        location (google.maps.places_v1.types.SearchTextRequest.Location):
            The region to search. Setting location would usually yields
            better results. Recommended to set. This location serves as
            a bias unless strict_restriction is set to true, which turns
            the location to a strict restriction.

            Deprecated. Use LocationRestriction or LocationBias instead.
        included_type (str):
            The requested place type. Full list of types supported:
            https://developers.google.com/places/supported_types. Only
            support one included type.
        open_now (bool):
            Used to restrict the search to places that are open at a
            specific time. open_now marks if a business is currently
            open.
        price_range (google.maps.places_v1.types.Int32Range):
            [Deprecated!]Used to restrict the search to places that are
            within a certain price range. This is on a scale of 0 to 4.
            Set a minimum of 0 or set a maximum of 4 has no effect on
            the search results. Min price is default to 0 and max price
            is default to 4. Default value will be used if either min or
            max is unset.
        min_rating (float):
            Filter out results whose average user rating is strictly
            less than this limit. A valid value must be an float between
            0 and 5 (inclusively) at a 0.5 cadence i.e.
            ``[0, 0.5, 1.0, ... , 5.0]`` inclusively. This is to keep
            parity with LocalRefinement_UserRating. The input rating
            will round up to the nearest 0.5(ceiling). For instance, a
            rating of 0.6 will eliminate all results with a less than
            1.0 rating.
        max_result_count (int):
            Maximum number of results to return. It must be between 1
            and 20, inclusively. If the number is unset, it falls back
            to the upper limit. If the number is set to negative or
            exceeds the upper limit, an INVALID_ARGUMENT error is
            returned.
        price_levels (MutableSequence[google.maps.places_v1.types.PriceLevel]):
            Used to restrict the search to places that
            are marked as certain price levels. Users can
            choose any combinations of price levels. Default
            to select all price levels.
        strict_type_filtering (bool):
            Used to set strict type filtering for included_type. If set
            to true, only results of the same type will be returned.
            Default to false.
        location_bias (google.maps.places_v1.types.SearchTextRequest.LocationBias):
            The region to search. This location serves as a bias which
            means results around given location might be returned.
            Cannot be set along with location_restriction.
        location_restriction (google.maps.places_v1.types.SearchTextRequest.LocationRestriction):
            The region to search. This location serves as a restriction
            which means results outside given location will not be
            returned. Cannot be set along with location_bias.
    """

    class RankPreference(proto.Enum):
        r"""How results will be ranked in the response.

        Values:
            RANK_PREFERENCE_UNSPECIFIED (0):
                RankPreference value not set. Will default to
                DISTANCE.
            DISTANCE (1):
                Ranks results by distance.
            RELEVANCE (2):
                Ranks results by relevance. Sort order
                determined by normal ranking stack. See
                SortRefinement::RELEVANCE.
        """
        RANK_PREFERENCE_UNSPECIFIED = 0
        DISTANCE = 1
        RELEVANCE = 2

    class Location(proto.Message):
        r"""The region to search.
        Deprecated. Use LocationRestriction or LocationBias instead.


        .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

        Attributes:
            rectangle (google.geo.type.types.Viewport):
                A rectangle box defined by northeast and
                southwest corner.

                This field is a member of `oneof`_ ``type``.
            strict_restriction (bool):
                Make location field a strict restriction and
                filter out POIs outside of the given location.
                If location type field is unset this field will
                have no effect.
        """

        rectangle: viewport.Viewport = proto.Field(
            proto.MESSAGE,
            number=1,
            oneof="type",
            message=viewport.Viewport,
        )
        strict_restriction: bool = proto.Field(
            proto.BOOL,
            number=2,
        )

    class LocationBias(proto.Message):
        r"""The region to search. This location serves as a bias which
        means results around given location might be returned.

        This message has `oneof`_ fields (mutually exclusive fields).
        For each oneof, at most one member field can be set at the same time.
        Setting any member of the oneof automatically clears all other
        members.

        .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

        Attributes:
            rectangle (google.geo.type.types.Viewport):
                A rectangle box defined by northeast and
                southwest corner.

                This field is a member of `oneof`_ ``type``.
            circle (google.maps.places_v1.types.Circle):
                A circle defined by center point and radius.

                This field is a member of `oneof`_ ``type``.
        """

        rectangle: viewport.Viewport = proto.Field(
            proto.MESSAGE,
            number=1,
            oneof="type",
            message=viewport.Viewport,
        )
        circle: geometry.Circle = proto.Field(
            proto.MESSAGE,
            number=2,
            oneof="type",
            message=geometry.Circle,
        )

    class LocationRestriction(proto.Message):
        r"""The region to search. This location serves as a restriction
        which means results outside given location will not be returned.


        .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

        Attributes:
            rectangle (google.geo.type.types.Viewport):
                A rectangle box defined by northeast and
                southwest corner.

                This field is a member of `oneof`_ ``type``.
        """

        rectangle: viewport.Viewport = proto.Field(
            proto.MESSAGE,
            number=1,
            oneof="type",
            message=viewport.Viewport,
        )

    text_query: str = proto.Field(
        proto.STRING,
        number=1,
    )
    language_code: str = proto.Field(
        proto.STRING,
        number=2,
    )
    region_code: str = proto.Field(
        proto.STRING,
        number=3,
    )
    rank_preference: RankPreference = proto.Field(
        proto.ENUM,
        number=4,
        enum=RankPreference,
    )
    location: Location = proto.Field(
        proto.MESSAGE,
        number=5,
        message=Location,
    )
    included_type: str = proto.Field(
        proto.STRING,
        number=6,
    )
    open_now: bool = proto.Field(
        proto.BOOL,
        number=7,
    )
    price_range: "Int32Range" = proto.Field(
        proto.MESSAGE,
        number=8,
        message="Int32Range",
    )
    min_rating: float = proto.Field(
        proto.DOUBLE,
        number=9,
    )
    max_result_count: int = proto.Field(
        proto.INT32,
        number=10,
    )
    price_levels: MutableSequence[place.PriceLevel] = proto.RepeatedField(
        proto.ENUM,
        number=11,
        enum=place.PriceLevel,
    )
    strict_type_filtering: bool = proto.Field(
        proto.BOOL,
        number=12,
    )
    location_bias: LocationBias = proto.Field(
        proto.MESSAGE,
        number=13,
        message=LocationBias,
    )
    location_restriction: LocationRestriction = proto.Field(
        proto.MESSAGE,
        number=14,
        message=LocationRestriction,
    )


class SearchTextResponse(proto.Message):
    r"""Response proto for SearchText.

    Attributes:
        places (MutableSequence[google.maps.places_v1.types.Place]):
            A list of places that meet the user's text
            search criteria.
    """

    places: MutableSequence[place.Place] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message=place.Place,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
