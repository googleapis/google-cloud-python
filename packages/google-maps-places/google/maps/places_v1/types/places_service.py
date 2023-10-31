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
        "SearchNearbyRequest",
        "SearchNearbyResponse",
        "SearchTextRequest",
        "SearchTextResponse",
        "GetPhotoMediaRequest",
        "PhotoMedia",
        "GetPlaceRequest",
    },
)


class SearchNearbyRequest(proto.Message):
    r"""Request proto for Search Nearby.

    Attributes:
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
            the request is coming from. This parameter is used to
            display the place details, like region-specific place name,
            if available. The parameter can affect results based on
            applicable law.

            For more information, see
            http://www.unicode.org/reports/tr35/#unicode_region_subtag.

            Note that 3-digit region codes are not currently supported.
        included_types (MutableSequence[str]):
            Included Place type (eg, "restaurant" or "gas_station") from
            https://developers.google.com/places/supported_types.

            If there are any conflicting types, i.e. a type appears in
            both included_types and excluded_types, an INVALID_ARGUMENT
            error is returned.

            If a Place type is specified with multiple type
            restrictions, only places that satisfy all of the
            restrictions are returned. For example, if we have
            {included_types = ["restaurant"], excluded_primary_types =
            ["restaurant"]}, the returned places are POIs that provide
            "restaurant" related services but do not operate primarily
            as "restaurants".
        excluded_types (MutableSequence[str]):
            Excluded Place type (eg, "restaurant" or "gas_station") from
            https://developers.google.com/places/supported_types.

            If the client provides both included_types (e.g. restaurant)
            and excluded_types (e.g. cafe), then the response should
            include places that are restaurant but not cafe. The
            response includes places that match at least one of the
            included_types and none of the excluded_types.

            If there are any conflicting types, i.e. a type appears in
            both included_types and excluded_types, an INVALID_ARGUMENT
            error is returned.

            If a Place type is specified with multiple type
            restrictions, only places that satisfy all of the
            restrictions are returned. For example, if we have
            {included_types = ["restaurant"], excluded_primary_types =
            ["restaurant"]}, the returned places are POIs that provide
            "restaurant" related services but do not operate primarily
            as "restaurants".
        included_primary_types (MutableSequence[str]):
            Included primary Place type (e.g. "restaurant" or
            "gas_station") from
            https://developers.google.com/places/supported_types.

            If there are any conflicting primary types, i.e. a type
            appears in both included_primary_types and
            excluded_primary_types, an INVALID_ARGUMENT error is
            returned.

            If a Place type is specified with multiple type
            restrictions, only places that satisfy all of the
            restrictions are returned. For example, if we have
            {included_types = ["restaurant"], excluded_primary_types =
            ["restaurant"]}, the returned places are POIs that provide
            "restaurant" related services but do not operate primarily
            as "restaurants".
        excluded_primary_types (MutableSequence[str]):
            Excluded primary Place type (e.g. "restaurant" or
            "gas_station") from
            https://developers.google.com/places/supported_types.

            If there are any conflicting primary types, i.e. a type
            appears in both included_primary_types and
            excluded_primary_types, an INVALID_ARGUMENT error is
            returned.

            If a Place type is specified with multiple type
            restrictions, only places that satisfy all of the
            restrictions are returned. For example, if we have
            {included_types = ["restaurant"], excluded_primary_types =
            ["restaurant"]}, the returned places are POIs that provide
            "restaurant" related services but do not operate primarily
            as "restaurants".
        max_result_count (int):
            Maximum number of results to return. It must be between 1
            and 20, inclusively. If the number is unset, it falls back
            to the upper limit. If the number is set to negative or
            exceeds the upper limit, an INVALID_ARGUMENT error is
            returned.
        location_restriction (google.maps.places_v1.types.SearchNearbyRequest.LocationRestriction):
            Required. The region to search.
        rank_preference (google.maps.places_v1.types.SearchNearbyRequest.RankPreference):
            How results will be ranked in the response.
    """

    class RankPreference(proto.Enum):
        r"""How results will be ranked in the response.

        Values:
            RANK_PREFERENCE_UNSPECIFIED (0):
                RankPreference value not set. Will use rank
                by POPULARITY by default.
            DISTANCE (1):
                Ranks results by distance.
            POPULARITY (2):
                Ranks results by popularity.
        """
        RANK_PREFERENCE_UNSPECIFIED = 0
        DISTANCE = 1
        POPULARITY = 2

    class LocationRestriction(proto.Message):
        r"""The region to search.

        .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

        Attributes:
            circle (google.maps.places_v1.types.Circle):
                A circle defined by center point and radius.

                This field is a member of `oneof`_ ``type``.
        """

        circle: geometry.Circle = proto.Field(
            proto.MESSAGE,
            number=2,
            oneof="type",
            message=geometry.Circle,
        )

    language_code: str = proto.Field(
        proto.STRING,
        number=1,
    )
    region_code: str = proto.Field(
        proto.STRING,
        number=2,
    )
    included_types: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=3,
    )
    excluded_types: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=4,
    )
    included_primary_types: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=5,
    )
    excluded_primary_types: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=6,
    )
    max_result_count: int = proto.Field(
        proto.INT32,
        number=7,
    )
    location_restriction: LocationRestriction = proto.Field(
        proto.MESSAGE,
        number=8,
        message=LocationRestriction,
    )
    rank_preference: RankPreference = proto.Field(
        proto.ENUM,
        number=9,
        enum=RankPreference,
    )


class SearchNearbyResponse(proto.Message):
    r"""Response proto for Search Nearby.

    Attributes:
        places (MutableSequence[google.maps.places_v1.types.Place]):
            A list of interesting places that meets
            user's requirements like places types, number of
            places and specific location restriction.
    """

    places: MutableSequence[place.Place] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message=place.Place,
    )


class SearchTextRequest(proto.Message):
    r"""Request proto for SearchText.

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
            the request is coming from. This parameter is used to
            display the place details, like region-specific place name,
            if available. The parameter can affect results based on
            applicable law.

            For more information, see
            http://www.unicode.org/reports/tr35/#unicode_region_subtag.

            Note that 3-digit region codes are not currently supported.
        rank_preference (google.maps.places_v1.types.SearchTextRequest.RankPreference):
            How results will be ranked in the response.
        included_type (str):
            The requested place type. Full list of types supported:
            https://developers.google.com/places/supported_types. Only
            support one included type.
        open_now (bool):
            Used to restrict the search to places that are open at a
            specific time. open_now marks if a business is currently
            open.
        min_rating (float):
            Filter out results whose average user rating is strictly
            less than this limit. A valid value must be an float between
            0 and 5 (inclusively) at a 0.5 cadence i.e. [0, 0.5, 1.0,
            ... , 5.0] inclusively. This is to keep parity with
            LocalRefinement_UserRating. The input rating will round up
            to the nearest 0.5(ceiling). For instance, a rating of 0.6
            will eliminate all results with a less than 1.0 rating.
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
    included_type: str = proto.Field(
        proto.STRING,
        number=6,
    )
    open_now: bool = proto.Field(
        proto.BOOL,
        number=7,
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


class GetPhotoMediaRequest(proto.Message):
    r"""Request for fetching a photo of a place using a photo
    resource name.

    Attributes:
        name (str):
            Required. The resource name of a photo. It is returned in
            Place's photos.name field. Format:
            places/<place_id>/photos/<photo_reference>/media.
        max_width_px (int):
            Optional. Specifies the maximum desired width, in pixels, of
            the image. If the image is smaller than the values
            specified, the original image will be returned. If the image
            is larger in either dimension, it will be scaled to match
            the smaller of the two dimensions, restricted to its
            original aspect ratio. Both the max_height_px and
            max_width_px properties accept an integer between 1 and
            4800, inclusively. If the value is not within the allowed
            range, an INVALID_ARGUMENT error will be returned.

            At least one of max_height_px or max_width_px needs to be
            specified. If neither max_height_px nor max_width_px is
            specified, an INVALID_ARGUMENT error will be returned.
        max_height_px (int):
            Optional. Specifies the maximum desired height, in pixels,
            of the image. If the image is smaller than the values
            specified, the original image will be returned. If the image
            is larger in either dimension, it will be scaled to match
            the smaller of the two dimensions, restricted to its
            original aspect ratio. Both the max_height_px and
            max_width_px properties accept an integer between 1 and
            4800, inclusively. If the value is not within the allowed
            range, an INVALID_ARGUMENT error will be returned.

            At least one of max_height_px or max_width_px needs to be
            specified. If neither max_height_px nor max_width_px is
            specified, an INVALID_ARGUMENT error will be returned.
        skip_http_redirect (bool):
            Optional. If set, skip the default HTTP
            redirect behavior and render a text format (for
            example, in JSON format for HTTP use case)
            response. If not set, an HTTP redirect will be
            issued to redirect the call to the image midea.
            This option is ignored for non-HTTP requests.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    max_width_px: int = proto.Field(
        proto.INT32,
        number=2,
    )
    max_height_px: int = proto.Field(
        proto.INT32,
        number=3,
    )
    skip_http_redirect: bool = proto.Field(
        proto.BOOL,
        number=4,
    )


class PhotoMedia(proto.Message):
    r"""A photo media from Places API.

    Attributes:
        name (str):
            The resource name of a photo. It is returned in Place's
            photos.name field. Format:
            places/<place_id>/photos/<photo_reference>/media.
        photo_uri (str):
            A short-lived uri that can be used to render
            the photo.
    """

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    photo_uri: str = proto.Field(
        proto.STRING,
        number=2,
    )


class GetPlaceRequest(proto.Message):
    r"""Request for fetching a Place with a place id (in a name)
    string.

    Attributes:
        name (str):
            Required. A place_id returned in a Place (with "places/"
            prefix), or equivalently the name in the same Place. Format:
            places/<place_id>.
        language_code (str):
            Optional. Place details will be displayed
            with the preferred language if available.

            Current list of supported languages:

            https://developers.google.com/maps/faq#languagesupport.
        region_code (str):
            Optional. The Unicode country/region code (CLDR) of the
            location where the request is coming from. This parameter is
            used to display the place details, like region-specific
            place name, if available. The parameter can affect results
            based on applicable law. For more information, see
            http://www.unicode.org/reports/tr35/#unicode_region_subtag.

            Note that 3-digit region codes are not currently supported.
    """

    name: str = proto.Field(
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


__all__ = tuple(sorted(__protobuf__.manifest))
