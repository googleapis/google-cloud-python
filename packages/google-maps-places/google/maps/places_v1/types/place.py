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

from google.geo.type.types import viewport as ggt_viewport
from google.type import date_pb2  # type: ignore
from google.type import latlng_pb2  # type: ignore
from google.type import localized_text_pb2  # type: ignore
import proto  # type: ignore

from google.maps.places_v1.types import content_block, ev_charging
from google.maps.places_v1.types import fuel_options as gmp_fuel_options
from google.maps.places_v1.types import photo, reference, review

__protobuf__ = proto.module(
    package="google.maps.places.v1",
    manifest={
        "PriceLevel",
        "Place",
    },
)


class PriceLevel(proto.Enum):
    r"""Price level of the place.

    Values:
        PRICE_LEVEL_UNSPECIFIED (0):
            Place price level is unspecified or unknown.
        PRICE_LEVEL_FREE (1):
            Place provides free services.
        PRICE_LEVEL_INEXPENSIVE (2):
            Place provides inexpensive services.
        PRICE_LEVEL_MODERATE (3):
            Place provides moderately priced services.
        PRICE_LEVEL_EXPENSIVE (4):
            Place provides expensive services.
        PRICE_LEVEL_VERY_EXPENSIVE (5):
            Place provides very expensive services.
    """
    PRICE_LEVEL_UNSPECIFIED = 0
    PRICE_LEVEL_FREE = 1
    PRICE_LEVEL_INEXPENSIVE = 2
    PRICE_LEVEL_MODERATE = 3
    PRICE_LEVEL_EXPENSIVE = 4
    PRICE_LEVEL_VERY_EXPENSIVE = 5


class Place(proto.Message):
    r"""All the information representing a Place.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        name (str):
            This Place's resource name, in ``places/{place_id}`` format.
            Can be used to look up the Place.
        id (str):
            The unique identifier of a place.
        display_name (google.type.localized_text_pb2.LocalizedText):
            The localized name of the place, suitable as
            a short human-readable description. For example,
            "Google Sydney", "Starbucks", "Pyrmont", etc.
        types (MutableSequence[str]):
            A set of type tags for this result. For
            example, "political" and "locality". For the
            complete list of possible values, see Table A
            and Table B at
            https://developers.google.com/maps/documentation/places/web-service/place-types
        primary_type (str):
            The primary type of the given result. This
            type must one of the Places API supported types.
            For example, "restaurant", "cafe", "airport",
            etc.  A place can only have a single primary
            type.  For the complete list of possible values,
            see Table A and Table B at
            https://developers.google.com/maps/documentation/places/web-service/place-types
        primary_type_display_name (google.type.localized_text_pb2.LocalizedText):
            The display name of the primary type,
            localized to the request language if applicable.
            For the complete list of possible values, see
            Table A and Table B at
            https://developers.google.com/maps/documentation/places/web-service/place-types
        national_phone_number (str):
            A human-readable phone number for the place,
            in national format.
        international_phone_number (str):
            A human-readable phone number for the place,
            in international format.
        formatted_address (str):
            A full, human-readable address for this
            place.
        short_formatted_address (str):
            A short, human-readable address for this
            place.
        address_components (MutableSequence[google.maps.places_v1.types.Place.AddressComponent]):
            Repeated components for each locality level. Note the
            following facts about the address_components[] array:

            -  The array of address components may contain more
               components than the formatted_address.
            -  The array does not necessarily include all the political
               entities that contain an address, apart from those
               included in the formatted_address. To retrieve all the
               political entities that contain a specific address, you
               should use reverse geocoding, passing the
               latitude/longitude of the address as a parameter to the
               request.
            -  The format of the response is not guaranteed to remain
               the same between requests. In particular, the number of
               address_components varies based on the address requested
               and can change over time for the same address. A
               component can change position in the array. The type of
               the component can change. A particular component may be
               missing in a later response.
        plus_code (google.maps.places_v1.types.Place.PlusCode):
            Plus code of the place location lat/long.
        location (google.type.latlng_pb2.LatLng):
            The position of this place.
        viewport (google.geo.type.types.Viewport):
            A viewport suitable for displaying the place
            on an average-sized map.
        rating (float):
            A rating between 1.0 and 5.0, based on user
            reviews of this place.
        google_maps_uri (str):
            A URL providing more information about this
            place.
        website_uri (str):
            The authoritative website for this place,
            e.g. a business' homepage. Note that for places
            that are part of a chain (e.g. an IKEA store),
            this will usually be the website for the
            individual store, not the overall chain.
        reviews (MutableSequence[google.maps.places_v1.types.Review]):
            List of reviews about this place, sorted by
            relevance. A maximum of 5 reviews can be
            returned.
        regular_opening_hours (google.maps.places_v1.types.Place.OpeningHours):
            The regular hours of operation.
        utc_offset_minutes (int):
            Number of minutes this place's timezone is
            currently offset from UTC. This is expressed in
            minutes to support timezones that are offset by
            fractions of an hour, e.g. X hours and 15
            minutes.

            This field is a member of `oneof`_ ``_utc_offset_minutes``.
        photos (MutableSequence[google.maps.places_v1.types.Photo]):
            Information (including references) about
            photos of this place. A maximum of 10 photos can
            be returned.
        adr_format_address (str):
            The place's address in adr microformat:
            http://microformats.org/wiki/adr.
        business_status (google.maps.places_v1.types.Place.BusinessStatus):
            The business status for the place.
        price_level (google.maps.places_v1.types.PriceLevel):
            Price level of the place.
        attributions (MutableSequence[google.maps.places_v1.types.Place.Attribution]):
            A set of data provider that must be shown
            with this result.
        user_rating_count (int):
            The total number of reviews (with or without
            text) for this place.

            This field is a member of `oneof`_ ``_user_rating_count``.
        icon_mask_base_uri (str):
            A truncated URL to an icon mask. User can
            access different icon type by appending type
            suffix to the end (eg, ".svg" or ".png").
        icon_background_color (str):
            Background color for icon_mask in hex format, e.g. #909CE1.
        takeout (bool):
            Specifies if the business supports takeout.

            This field is a member of `oneof`_ ``_takeout``.
        delivery (bool):
            Specifies if the business supports delivery.

            This field is a member of `oneof`_ ``_delivery``.
        dine_in (bool):
            Specifies if the business supports indoor or
            outdoor seating options.

            This field is a member of `oneof`_ ``_dine_in``.
        curbside_pickup (bool):
            Specifies if the business supports curbside
            pickup.

            This field is a member of `oneof`_ ``_curbside_pickup``.
        reservable (bool):
            Specifies if the place supports reservations.

            This field is a member of `oneof`_ ``_reservable``.
        serves_breakfast (bool):
            Specifies if the place serves breakfast.

            This field is a member of `oneof`_ ``_serves_breakfast``.
        serves_lunch (bool):
            Specifies if the place serves lunch.

            This field is a member of `oneof`_ ``_serves_lunch``.
        serves_dinner (bool):
            Specifies if the place serves dinner.

            This field is a member of `oneof`_ ``_serves_dinner``.
        serves_beer (bool):
            Specifies if the place serves beer.

            This field is a member of `oneof`_ ``_serves_beer``.
        serves_wine (bool):
            Specifies if the place serves wine.

            This field is a member of `oneof`_ ``_serves_wine``.
        serves_brunch (bool):
            Specifies if the place serves brunch.

            This field is a member of `oneof`_ ``_serves_brunch``.
        serves_vegetarian_food (bool):
            Specifies if the place serves vegetarian
            food.

            This field is a member of `oneof`_ ``_serves_vegetarian_food``.
        current_opening_hours (google.maps.places_v1.types.Place.OpeningHours):
            The hours of operation for the next seven days (including
            today). The time period starts at midnight on the date of
            the request and ends at 11:59 pm six days later. This field
            includes the special_days subfield of all hours, set for
            dates that have exceptional hours.
        current_secondary_opening_hours (MutableSequence[google.maps.places_v1.types.Place.OpeningHours]):
            Contains an array of entries for the next seven days
            including information about secondary hours of a business.
            Secondary hours are different from a business's main hours.
            For example, a restaurant can specify drive through hours or
            delivery hours as its secondary hours. This field populates
            the type subfield, which draws from a predefined list of
            opening hours types (such as DRIVE_THROUGH, PICKUP, or
            TAKEOUT) based on the types of the place. This field
            includes the special_days subfield of all hours, set for
            dates that have exceptional hours.
        regular_secondary_opening_hours (MutableSequence[google.maps.places_v1.types.Place.OpeningHours]):
            Contains an array of entries for information about regular
            secondary hours of a business. Secondary hours are different
            from a business's main hours. For example, a restaurant can
            specify drive through hours or delivery hours as its
            secondary hours. This field populates the type subfield,
            which draws from a predefined list of opening hours types
            (such as DRIVE_THROUGH, PICKUP, or TAKEOUT) based on the
            types of the place.
        editorial_summary (google.type.localized_text_pb2.LocalizedText):
            Contains a summary of the place. A summary is
            comprised of a textual overview, and also
            includes the language code for these if
            applicable. Summary text must be presented as-is
            and can not be modified or altered.
        outdoor_seating (bool):
            Place provides outdoor seating.

            This field is a member of `oneof`_ ``_outdoor_seating``.
        live_music (bool):
            Place provides live music.

            This field is a member of `oneof`_ ``_live_music``.
        menu_for_children (bool):
            Place has a children's menu.

            This field is a member of `oneof`_ ``_menu_for_children``.
        serves_cocktails (bool):
            Place serves cocktails.

            This field is a member of `oneof`_ ``_serves_cocktails``.
        serves_dessert (bool):
            Place serves dessert.

            This field is a member of `oneof`_ ``_serves_dessert``.
        serves_coffee (bool):
            Place serves coffee.

            This field is a member of `oneof`_ ``_serves_coffee``.
        good_for_children (bool):
            Place is good for children.

            This field is a member of `oneof`_ ``_good_for_children``.
        allows_dogs (bool):
            Place allows dogs.

            This field is a member of `oneof`_ ``_allows_dogs``.
        restroom (bool):
            Place has restroom.

            This field is a member of `oneof`_ ``_restroom``.
        good_for_groups (bool):
            Place accommodates groups.

            This field is a member of `oneof`_ ``_good_for_groups``.
        good_for_watching_sports (bool):
            Place is suitable for watching sports.

            This field is a member of `oneof`_ ``_good_for_watching_sports``.
        payment_options (google.maps.places_v1.types.Place.PaymentOptions):
            Payment options the place accepts. If a
            payment option data is not available, the
            payment option field will be unset.
        parking_options (google.maps.places_v1.types.Place.ParkingOptions):
            Options of parking provided by the place.
        sub_destinations (MutableSequence[google.maps.places_v1.types.Place.SubDestination]):
            A list of sub destinations related to the
            place.
        accessibility_options (google.maps.places_v1.types.Place.AccessibilityOptions):
            Information about the accessibility options a
            place offers.

            This field is a member of `oneof`_ ``_accessibility_options``.
        fuel_options (google.maps.places_v1.types.FuelOptions):
            The most recent information about fuel
            options in a gas station. This information is
            updated regularly.
        ev_charge_options (google.maps.places_v1.types.EVChargeOptions):
            Information of ev charging options.
        generative_summary (google.maps.places_v1.types.Place.GenerativeSummary):
            Experimental: See
            https://developers.google.com/maps/documentation/places/web-service/experimental/places-generative
            for more details.

            AI-generated summary of the place.
        area_summary (google.maps.places_v1.types.Place.AreaSummary):
            Experimental: See
            https://developers.google.com/maps/documentation/places/web-service/experimental/places-generative
            for more details.

            AI-generated summary of the area that the place
            is in.
    """

    class BusinessStatus(proto.Enum):
        r"""Business status for the place.

        Values:
            BUSINESS_STATUS_UNSPECIFIED (0):
                Default value. This value is unused.
            OPERATIONAL (1):
                The establishment is operational, not
                necessarily open now.
            CLOSED_TEMPORARILY (2):
                The establishment is temporarily closed.
            CLOSED_PERMANENTLY (3):
                The establishment is permanently closed.
        """
        BUSINESS_STATUS_UNSPECIFIED = 0
        OPERATIONAL = 1
        CLOSED_TEMPORARILY = 2
        CLOSED_PERMANENTLY = 3

    class AddressComponent(proto.Message):
        r"""The structured components that form the formatted address, if
        this information is available.

        Attributes:
            long_text (str):
                The full text description or name of the address component.
                For example, an address component for the country Australia
                may have a long_name of "Australia".
            short_text (str):
                An abbreviated textual name for the address component, if
                available. For example, an address component for the country
                of Australia may have a short_name of "AU".
            types (MutableSequence[str]):
                An array indicating the type(s) of the
                address component.
            language_code (str):
                The language used to format this components,
                in CLDR notation.
        """

        long_text: str = proto.Field(
            proto.STRING,
            number=1,
        )
        short_text: str = proto.Field(
            proto.STRING,
            number=2,
        )
        types: MutableSequence[str] = proto.RepeatedField(
            proto.STRING,
            number=3,
        )
        language_code: str = proto.Field(
            proto.STRING,
            number=4,
        )

    class PlusCode(proto.Message):
        r"""Plus code (http://plus.codes) is a location reference with
        two formats: global code defining a 14mx14m (1/8000th of a
        degree) or smaller rectangle, and compound code, replacing the
        prefix with a reference location.

        Attributes:
            global_code (str):
                Place's global (full) code, such as
                "9FWM33GV+HQ", representing an 1/8000 by 1/8000
                degree area (~14 by 14 meters).
            compound_code (str):
                Place's compound code, such as "33GV+HQ,
                Ramberg, Norway", containing the suffix of the
                global code and replacing the prefix with a
                formatted name of a reference entity.
        """

        global_code: str = proto.Field(
            proto.STRING,
            number=1,
        )
        compound_code: str = proto.Field(
            proto.STRING,
            number=2,
        )

    class OpeningHours(proto.Message):
        r"""Information about business hour of the place.

        .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

        Attributes:
            open_now (bool):
                Is this place open right now?  Always present
                unless we lack time-of-day or timezone data for
                these opening hours.

                This field is a member of `oneof`_ ``_open_now``.
            periods (MutableSequence[google.maps.places_v1.types.Place.OpeningHours.Period]):
                The periods that this place is open during
                the week. The periods are in chronological
                order, starting with Sunday in the place-local
                timezone. An empty (but not absent) value
                indicates a place that is never open, e.g.
                because it is closed temporarily for
                renovations.
            weekday_descriptions (MutableSequence[str]):
                Localized strings describing the opening
                hours of this place, one string for each day of
                the week.  Will be empty if the hours are
                unknown or could not be converted to localized
                text. Example: "Sun: 18:00–06:00".
            secondary_hours_type (google.maps.places_v1.types.Place.OpeningHours.SecondaryHoursType):
                A type string used to identify the type of
                secondary hours.
            special_days (MutableSequence[google.maps.places_v1.types.Place.OpeningHours.SpecialDay]):
                Structured information for special days that fall within the
                period that the returned opening hours cover. Special days
                are days that could impact the business hours of a place,
                e.g. Christmas day. Set for current_opening_hours and
                current_secondary_opening_hours if there are exceptional
                hours.
        """

        class SecondaryHoursType(proto.Enum):
            r"""A type used to identify the type of secondary hours.

            Values:
                SECONDARY_HOURS_TYPE_UNSPECIFIED (0):
                    Default value when secondary hour type is not
                    specified.
                DRIVE_THROUGH (1):
                    The drive-through hour for banks,
                    restaurants, or pharmacies.
                HAPPY_HOUR (2):
                    The happy hour.
                DELIVERY (3):
                    The delivery hour.
                TAKEOUT (4):
                    The takeout hour.
                KITCHEN (5):
                    The kitchen hour.
                BREAKFAST (6):
                    The breakfast hour.
                LUNCH (7):
                    The lunch hour.
                DINNER (8):
                    The dinner hour.
                BRUNCH (9):
                    The brunch hour.
                PICKUP (10):
                    The pickup hour.
                ACCESS (11):
                    The access hours for storage places.
                SENIOR_HOURS (12):
                    The special hours for seniors.
                ONLINE_SERVICE_HOURS (13):
                    The online service hours.
            """
            SECONDARY_HOURS_TYPE_UNSPECIFIED = 0
            DRIVE_THROUGH = 1
            HAPPY_HOUR = 2
            DELIVERY = 3
            TAKEOUT = 4
            KITCHEN = 5
            BREAKFAST = 6
            LUNCH = 7
            DINNER = 8
            BRUNCH = 9
            PICKUP = 10
            ACCESS = 11
            SENIOR_HOURS = 12
            ONLINE_SERVICE_HOURS = 13

        class Period(proto.Message):
            r"""A period the place remains in open_now status.

            Attributes:
                open_ (google.maps.places_v1.types.Place.OpeningHours.Period.Point):
                    The time that the place starts to be open.
                close (google.maps.places_v1.types.Place.OpeningHours.Period.Point):
                    The time that the place starts to be closed.
            """

            class Point(proto.Message):
                r"""Status changing points.

                .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

                Attributes:
                    day (int):
                        A day of the week, as an integer in the range
                        0-6.  0 is Sunday, 1 is Monday, etc.

                        This field is a member of `oneof`_ ``_day``.
                    hour (int):
                        The hour in 2 digits. Ranges from 00 to 23.

                        This field is a member of `oneof`_ ``_hour``.
                    minute (int):
                        The minute in 2 digits. Ranges from 00 to 59.

                        This field is a member of `oneof`_ ``_minute``.
                    date (google.type.date_pb2.Date):
                        Date in the local timezone for the place.
                    truncated (bool):
                        Whether or not this endpoint was truncated. Truncation
                        occurs when the real hours are outside the times we are
                        willing to return hours between, so we truncate the hours
                        back to these boundaries. This ensures that at most 24 \* 7
                        hours from midnight of the day of the request are returned.
                """

                day: int = proto.Field(
                    proto.INT32,
                    number=1,
                    optional=True,
                )
                hour: int = proto.Field(
                    proto.INT32,
                    number=2,
                    optional=True,
                )
                minute: int = proto.Field(
                    proto.INT32,
                    number=3,
                    optional=True,
                )
                date: date_pb2.Date = proto.Field(
                    proto.MESSAGE,
                    number=6,
                    message=date_pb2.Date,
                )
                truncated: bool = proto.Field(
                    proto.BOOL,
                    number=5,
                )

            open_: "Place.OpeningHours.Period.Point" = proto.Field(
                proto.MESSAGE,
                number=1,
                message="Place.OpeningHours.Period.Point",
            )
            close: "Place.OpeningHours.Period.Point" = proto.Field(
                proto.MESSAGE,
                number=2,
                message="Place.OpeningHours.Period.Point",
            )

        class SpecialDay(proto.Message):
            r"""Structured information for special days that fall within the
            period that the returned opening hours cover. Special days are
            days that could impact the business hours of a place, e.g.
            Christmas day.

            Attributes:
                date (google.type.date_pb2.Date):
                    The date of this special day.
            """

            date: date_pb2.Date = proto.Field(
                proto.MESSAGE,
                number=1,
                message=date_pb2.Date,
            )

        open_now: bool = proto.Field(
            proto.BOOL,
            number=1,
            optional=True,
        )
        periods: MutableSequence["Place.OpeningHours.Period"] = proto.RepeatedField(
            proto.MESSAGE,
            number=2,
            message="Place.OpeningHours.Period",
        )
        weekday_descriptions: MutableSequence[str] = proto.RepeatedField(
            proto.STRING,
            number=3,
        )
        secondary_hours_type: "Place.OpeningHours.SecondaryHoursType" = proto.Field(
            proto.ENUM,
            number=4,
            enum="Place.OpeningHours.SecondaryHoursType",
        )
        special_days: MutableSequence[
            "Place.OpeningHours.SpecialDay"
        ] = proto.RepeatedField(
            proto.MESSAGE,
            number=5,
            message="Place.OpeningHours.SpecialDay",
        )

    class Attribution(proto.Message):
        r"""Information about data providers of this place.

        Attributes:
            provider (str):
                Name of the Place's data provider.
            provider_uri (str):
                URI to the Place's data provider.
        """

        provider: str = proto.Field(
            proto.STRING,
            number=1,
        )
        provider_uri: str = proto.Field(
            proto.STRING,
            number=2,
        )

    class PaymentOptions(proto.Message):
        r"""Payment options the place accepts.

        .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

        Attributes:
            accepts_credit_cards (bool):
                Place accepts credit cards as payment.

                This field is a member of `oneof`_ ``_accepts_credit_cards``.
            accepts_debit_cards (bool):
                Place accepts debit cards as payment.

                This field is a member of `oneof`_ ``_accepts_debit_cards``.
            accepts_cash_only (bool):
                Place accepts cash only as payment. Places
                with this attribute may still accept other
                payment methods.

                This field is a member of `oneof`_ ``_accepts_cash_only``.
            accepts_nfc (bool):
                Place accepts NFC payments.

                This field is a member of `oneof`_ ``_accepts_nfc``.
        """

        accepts_credit_cards: bool = proto.Field(
            proto.BOOL,
            number=1,
            optional=True,
        )
        accepts_debit_cards: bool = proto.Field(
            proto.BOOL,
            number=2,
            optional=True,
        )
        accepts_cash_only: bool = proto.Field(
            proto.BOOL,
            number=3,
            optional=True,
        )
        accepts_nfc: bool = proto.Field(
            proto.BOOL,
            number=4,
            optional=True,
        )

    class ParkingOptions(proto.Message):
        r"""Information about parking options for the place. A parking
        lot could support more than one option at the same time.


        .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

        Attributes:
            free_parking_lot (bool):
                Place offers free parking lots.

                This field is a member of `oneof`_ ``_free_parking_lot``.
            paid_parking_lot (bool):
                Place offers paid parking lots.

                This field is a member of `oneof`_ ``_paid_parking_lot``.
            free_street_parking (bool):
                Place offers free street parking.

                This field is a member of `oneof`_ ``_free_street_parking``.
            paid_street_parking (bool):
                Place offers paid street parking.

                This field is a member of `oneof`_ ``_paid_street_parking``.
            valet_parking (bool):
                Place offers valet parking.

                This field is a member of `oneof`_ ``_valet_parking``.
            free_garage_parking (bool):
                Place offers free garage parking.

                This field is a member of `oneof`_ ``_free_garage_parking``.
            paid_garage_parking (bool):
                Place offers paid garage parking.

                This field is a member of `oneof`_ ``_paid_garage_parking``.
        """

        free_parking_lot: bool = proto.Field(
            proto.BOOL,
            number=1,
            optional=True,
        )
        paid_parking_lot: bool = proto.Field(
            proto.BOOL,
            number=2,
            optional=True,
        )
        free_street_parking: bool = proto.Field(
            proto.BOOL,
            number=3,
            optional=True,
        )
        paid_street_parking: bool = proto.Field(
            proto.BOOL,
            number=4,
            optional=True,
        )
        valet_parking: bool = proto.Field(
            proto.BOOL,
            number=5,
            optional=True,
        )
        free_garage_parking: bool = proto.Field(
            proto.BOOL,
            number=6,
            optional=True,
        )
        paid_garage_parking: bool = proto.Field(
            proto.BOOL,
            number=7,
            optional=True,
        )

    class SubDestination(proto.Message):
        r"""Place resource name and id of sub destinations that relate to
        the place. For example, different terminals are different
        destinations of an airport.

        Attributes:
            name (str):
                The resource name of the sub destination.
            id (str):
                The place id of the sub destination.
        """

        name: str = proto.Field(
            proto.STRING,
            number=1,
        )
        id: str = proto.Field(
            proto.STRING,
            number=2,
        )

    class AccessibilityOptions(proto.Message):
        r"""Information about the accessibility options a place offers.

        .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

        Attributes:
            wheelchair_accessible_parking (bool):
                Place offers wheelchair accessible parking.

                This field is a member of `oneof`_ ``_wheelchair_accessible_parking``.
            wheelchair_accessible_entrance (bool):
                Places has wheelchair accessible entrance.

                This field is a member of `oneof`_ ``_wheelchair_accessible_entrance``.
            wheelchair_accessible_restroom (bool):
                Place has wheelchair accessible restroom.

                This field is a member of `oneof`_ ``_wheelchair_accessible_restroom``.
            wheelchair_accessible_seating (bool):
                Place has wheelchair accessible seating.

                This field is a member of `oneof`_ ``_wheelchair_accessible_seating``.
        """

        wheelchair_accessible_parking: bool = proto.Field(
            proto.BOOL,
            number=1,
            optional=True,
        )
        wheelchair_accessible_entrance: bool = proto.Field(
            proto.BOOL,
            number=2,
            optional=True,
        )
        wheelchair_accessible_restroom: bool = proto.Field(
            proto.BOOL,
            number=3,
            optional=True,
        )
        wheelchair_accessible_seating: bool = proto.Field(
            proto.BOOL,
            number=4,
            optional=True,
        )

    class GenerativeSummary(proto.Message):
        r"""Experimental: See
        https://developers.google.com/maps/documentation/places/web-service/experimental/places-generative
        for more details.

        AI-generated summary of the place.

        Attributes:
            overview (google.type.localized_text_pb2.LocalizedText):
                The overview of the place.
            description (google.type.localized_text_pb2.LocalizedText):
                The detailed description of the place.
            references (google.maps.places_v1.types.References):
                References that are used to generate the
                summary description.
        """

        overview: localized_text_pb2.LocalizedText = proto.Field(
            proto.MESSAGE,
            number=1,
            message=localized_text_pb2.LocalizedText,
        )
        description: localized_text_pb2.LocalizedText = proto.Field(
            proto.MESSAGE,
            number=2,
            message=localized_text_pb2.LocalizedText,
        )
        references: reference.References = proto.Field(
            proto.MESSAGE,
            number=3,
            message=reference.References,
        )

    class AreaSummary(proto.Message):
        r"""Experimental: See
        https://developers.google.com/maps/documentation/places/web-service/experimental/places-generative
        for more details.

        AI-generated summary of the area that the place is in.

        Attributes:
            content_blocks (MutableSequence[google.maps.places_v1.types.ContentBlock]):
                Content blocks that compose the area summary.
                Each block has a separate topic about the area.
        """

        content_blocks: MutableSequence[
            content_block.ContentBlock
        ] = proto.RepeatedField(
            proto.MESSAGE,
            number=4,
            message=content_block.ContentBlock,
        )

    name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    id: str = proto.Field(
        proto.STRING,
        number=2,
    )
    display_name: localized_text_pb2.LocalizedText = proto.Field(
        proto.MESSAGE,
        number=31,
        message=localized_text_pb2.LocalizedText,
    )
    types: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=5,
    )
    primary_type: str = proto.Field(
        proto.STRING,
        number=50,
    )
    primary_type_display_name: localized_text_pb2.LocalizedText = proto.Field(
        proto.MESSAGE,
        number=32,
        message=localized_text_pb2.LocalizedText,
    )
    national_phone_number: str = proto.Field(
        proto.STRING,
        number=7,
    )
    international_phone_number: str = proto.Field(
        proto.STRING,
        number=8,
    )
    formatted_address: str = proto.Field(
        proto.STRING,
        number=9,
    )
    short_formatted_address: str = proto.Field(
        proto.STRING,
        number=51,
    )
    address_components: MutableSequence[AddressComponent] = proto.RepeatedField(
        proto.MESSAGE,
        number=10,
        message=AddressComponent,
    )
    plus_code: PlusCode = proto.Field(
        proto.MESSAGE,
        number=11,
        message=PlusCode,
    )
    location: latlng_pb2.LatLng = proto.Field(
        proto.MESSAGE,
        number=12,
        message=latlng_pb2.LatLng,
    )
    viewport: ggt_viewport.Viewport = proto.Field(
        proto.MESSAGE,
        number=13,
        message=ggt_viewport.Viewport,
    )
    rating: float = proto.Field(
        proto.DOUBLE,
        number=14,
    )
    google_maps_uri: str = proto.Field(
        proto.STRING,
        number=15,
    )
    website_uri: str = proto.Field(
        proto.STRING,
        number=16,
    )
    reviews: MutableSequence[review.Review] = proto.RepeatedField(
        proto.MESSAGE,
        number=53,
        message=review.Review,
    )
    regular_opening_hours: OpeningHours = proto.Field(
        proto.MESSAGE,
        number=21,
        message=OpeningHours,
    )
    utc_offset_minutes: int = proto.Field(
        proto.INT32,
        number=22,
        optional=True,
    )
    photos: MutableSequence[photo.Photo] = proto.RepeatedField(
        proto.MESSAGE,
        number=54,
        message=photo.Photo,
    )
    adr_format_address: str = proto.Field(
        proto.STRING,
        number=24,
    )
    business_status: BusinessStatus = proto.Field(
        proto.ENUM,
        number=25,
        enum=BusinessStatus,
    )
    price_level: "PriceLevel" = proto.Field(
        proto.ENUM,
        number=26,
        enum="PriceLevel",
    )
    attributions: MutableSequence[Attribution] = proto.RepeatedField(
        proto.MESSAGE,
        number=27,
        message=Attribution,
    )
    user_rating_count: int = proto.Field(
        proto.INT32,
        number=28,
        optional=True,
    )
    icon_mask_base_uri: str = proto.Field(
        proto.STRING,
        number=29,
    )
    icon_background_color: str = proto.Field(
        proto.STRING,
        number=30,
    )
    takeout: bool = proto.Field(
        proto.BOOL,
        number=33,
        optional=True,
    )
    delivery: bool = proto.Field(
        proto.BOOL,
        number=34,
        optional=True,
    )
    dine_in: bool = proto.Field(
        proto.BOOL,
        number=35,
        optional=True,
    )
    curbside_pickup: bool = proto.Field(
        proto.BOOL,
        number=36,
        optional=True,
    )
    reservable: bool = proto.Field(
        proto.BOOL,
        number=38,
        optional=True,
    )
    serves_breakfast: bool = proto.Field(
        proto.BOOL,
        number=39,
        optional=True,
    )
    serves_lunch: bool = proto.Field(
        proto.BOOL,
        number=40,
        optional=True,
    )
    serves_dinner: bool = proto.Field(
        proto.BOOL,
        number=41,
        optional=True,
    )
    serves_beer: bool = proto.Field(
        proto.BOOL,
        number=42,
        optional=True,
    )
    serves_wine: bool = proto.Field(
        proto.BOOL,
        number=43,
        optional=True,
    )
    serves_brunch: bool = proto.Field(
        proto.BOOL,
        number=44,
        optional=True,
    )
    serves_vegetarian_food: bool = proto.Field(
        proto.BOOL,
        number=45,
        optional=True,
    )
    current_opening_hours: OpeningHours = proto.Field(
        proto.MESSAGE,
        number=46,
        message=OpeningHours,
    )
    current_secondary_opening_hours: MutableSequence[
        OpeningHours
    ] = proto.RepeatedField(
        proto.MESSAGE,
        number=47,
        message=OpeningHours,
    )
    regular_secondary_opening_hours: MutableSequence[
        OpeningHours
    ] = proto.RepeatedField(
        proto.MESSAGE,
        number=49,
        message=OpeningHours,
    )
    editorial_summary: localized_text_pb2.LocalizedText = proto.Field(
        proto.MESSAGE,
        number=52,
        message=localized_text_pb2.LocalizedText,
    )
    outdoor_seating: bool = proto.Field(
        proto.BOOL,
        number=55,
        optional=True,
    )
    live_music: bool = proto.Field(
        proto.BOOL,
        number=56,
        optional=True,
    )
    menu_for_children: bool = proto.Field(
        proto.BOOL,
        number=57,
        optional=True,
    )
    serves_cocktails: bool = proto.Field(
        proto.BOOL,
        number=58,
        optional=True,
    )
    serves_dessert: bool = proto.Field(
        proto.BOOL,
        number=59,
        optional=True,
    )
    serves_coffee: bool = proto.Field(
        proto.BOOL,
        number=60,
        optional=True,
    )
    good_for_children: bool = proto.Field(
        proto.BOOL,
        number=62,
        optional=True,
    )
    allows_dogs: bool = proto.Field(
        proto.BOOL,
        number=63,
        optional=True,
    )
    restroom: bool = proto.Field(
        proto.BOOL,
        number=64,
        optional=True,
    )
    good_for_groups: bool = proto.Field(
        proto.BOOL,
        number=65,
        optional=True,
    )
    good_for_watching_sports: bool = proto.Field(
        proto.BOOL,
        number=66,
        optional=True,
    )
    payment_options: PaymentOptions = proto.Field(
        proto.MESSAGE,
        number=67,
        message=PaymentOptions,
    )
    parking_options: ParkingOptions = proto.Field(
        proto.MESSAGE,
        number=70,
        message=ParkingOptions,
    )
    sub_destinations: MutableSequence[SubDestination] = proto.RepeatedField(
        proto.MESSAGE,
        number=71,
        message=SubDestination,
    )
    accessibility_options: AccessibilityOptions = proto.Field(
        proto.MESSAGE,
        number=72,
        optional=True,
        message=AccessibilityOptions,
    )
    fuel_options: gmp_fuel_options.FuelOptions = proto.Field(
        proto.MESSAGE,
        number=78,
        message=gmp_fuel_options.FuelOptions,
    )
    ev_charge_options: ev_charging.EVChargeOptions = proto.Field(
        proto.MESSAGE,
        number=79,
        message=ev_charging.EVChargeOptions,
    )
    generative_summary: GenerativeSummary = proto.Field(
        proto.MESSAGE,
        number=80,
        message=GenerativeSummary,
    )
    area_summary: AreaSummary = proto.Field(
        proto.MESSAGE,
        number=81,
        message=AreaSummary,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
