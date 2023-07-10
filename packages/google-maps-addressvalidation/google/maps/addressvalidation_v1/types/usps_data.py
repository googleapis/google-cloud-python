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

import proto  # type: ignore

__protobuf__ = proto.module(
    package="google.maps.addressvalidation.v1",
    manifest={
        "UspsAddress",
        "UspsData",
    },
)


class UspsAddress(proto.Message):
    r"""USPS representation of a US address.

    Attributes:
        first_address_line (str):
            First address line.
        firm (str):
            Firm name.
        second_address_line (str):
            Second address line.
        urbanization (str):
            Puerto Rican urbanization name.
        city_state_zip_address_line (str):
            City + state + postal code.
        city (str):
            City name.
        state (str):
            2 letter state code.
        zip_code (str):
            Postal code e.g. 10009.
        zip_code_extension (str):
            4-digit postal code extension e.g. 5023.
    """

    first_address_line: str = proto.Field(
        proto.STRING,
        number=1,
    )
    firm: str = proto.Field(
        proto.STRING,
        number=2,
    )
    second_address_line: str = proto.Field(
        proto.STRING,
        number=3,
    )
    urbanization: str = proto.Field(
        proto.STRING,
        number=4,
    )
    city_state_zip_address_line: str = proto.Field(
        proto.STRING,
        number=5,
    )
    city: str = proto.Field(
        proto.STRING,
        number=6,
    )
    state: str = proto.Field(
        proto.STRING,
        number=7,
    )
    zip_code: str = proto.Field(
        proto.STRING,
        number=8,
    )
    zip_code_extension: str = proto.Field(
        proto.STRING,
        number=9,
    )


class UspsData(proto.Message):
    r"""The USPS data for the address. ``uspsData`` is not guaranteed to be
    fully populated for every US or PR address sent to the Address
    Validation API. It's recommended to integrate the backup address
    fields in the response if you utilize uspsData as the primary part
    of the response.

    Attributes:
        standardized_address (google.maps.addressvalidation_v1.types.UspsAddress):
            USPS standardized address.
        delivery_point_code (str):
            2 digit delivery point code
        delivery_point_check_digit (str):
            The delivery point check digit. This number is added to the
            end of the delivery_point_barcode for mechanically scanned
            mail. Adding all the digits of the delivery_point_barcode,
            delivery_point_check_digit, postal code, and ZIP+4 together
            should yield a number divisible by 10.
        dpv_confirmation (str):
            The possible values for DPV confirmation. Returns a single
            character.

            -  ``Y``: Address was DPV confirmed for primary and any
               secondary numbers.
            -  ``N``: Primary and any secondary number information
               failed to DPV confirm.
            -  ``S``: Address was DPV confirmed for the primary number
               only, and the secondary number information was present by
               not confirmed.
            -  ``D``: Address was DPV confirmed for the primary number
               only, and the secondary number information was missing.
        dpv_footnote (str):
            The footnotes from delivery point validation. Multiple
            footnotes may be strung together in the same string.

            -  ``AA``: Input address matched to the ZIP+4 file
            -  ``A1``: Input address was not matched to the ZIP+4 file
            -  ``BB``: Matched to DPV (all components)
            -  ``CC``: Secondary number not matched (present but
               invalid)
            -  ``N1``: High-rise address missing secondary number
            -  ``M1``: Primary number missing
            -  ``M3``: Primary number invalid
            -  ``P1``: Input address RR or HC box number missing
            -  ``P3``: Input address PO, RR, or HC Box number invalid
            -  ``F1``: Input address matched to a military address
            -  ``G1``: Input address matched to a general delivery
               address
            -  ``U1``: Input address matched to a unique ZIP code
            -  ``PB``: Input address matched to PBSA record
            -  ``RR``: DPV confirmed address with PMB information
            -  ``R1``: DPV confirmed address without PMB information
            -  ``R7``: Carrier Route R777 or R779 record
        dpv_cmra (str):
            Indicates if the address is a CMRA (Commercial Mail
            Receiving Agency)--a private business receiving mail for
            clients. Returns a single character.

            -  ``Y``: The address is a CMRA
            -  ``N``: The address is not a CMRA
        dpv_vacant (str):
            Is this place vacant? Returns a single character.

            -  ``Y``: The address is vacant
            -  ``N``: The address is not vacant
        dpv_no_stat (str):
            Is this a no stat address or an active address? No stat
            addresses are ones which are not continuously occupied or
            addresses that the USPS does not service. Returns a single
            character.

            -  ``Y``: The address is not active
            -  ``N``: The address is active
        carrier_route (str):
            The carrier route code. A four character code consisting of
            a one letter prefix and a three digit route designator.

            Prefixes:

            -  ``C``: Carrier route (or city route)
            -  ``R``: Rural route
            -  ``H``: Highway Contract Route
            -  ``B``: Post Office Box Section
            -  ``G``: General delivery unit
        carrier_route_indicator (str):
            Carrier route rate sort indicator.
        ews_no_match (bool):
            The delivery address is matchable, but the
            EWS file indicates that an exact match will be
            available soon.
        post_office_city (str):
            Main post office city.
        post_office_state (str):
            Main post office state.
        abbreviated_city (str):
            Abbreviated city.
        fips_county_code (str):
            FIPS county code.
        county (str):
            County name.
        elot_number (str):
            Enhanced Line of Travel (eLOT) number.
        elot_flag (str):
            eLOT Ascending/Descending Flag (A/D).
        lacs_link_return_code (str):
            LACSLink return code.
        lacs_link_indicator (str):
            LACSLink indicator.
        po_box_only_postal_code (bool):
            PO Box only postal code.
        suitelink_footnote (str):
            Footnotes from matching a street or highrise record to suite
            information. If business name match is found, the secondary
            number is returned.

            -  ``A``: SuiteLink record match, business address improved.
            -  ``00``: No match, business address is not improved.
        pmb_designator (str):
            PMB (Private Mail Box) unit designator.
        pmb_number (str):
            PMB (Private Mail Box) number;
        address_record_type (str):
            Type of the address record that matches the input address.

            -  ``F``: FIRM. This is a match to a Firm Record, which is
               the finest level of match available for an address.
            -  ``G``: GENERAL DELIVERY. This is a match to a General
               Delivery record.
            -  ``H``: BUILDING / APARTMENT. This is a match to a
               Building or Apartment record.
            -  ``P``: POST OFFICE BOX. This is a match to a Post Office
               Box.
            -  ``R``: RURAL ROUTE or HIGHWAY CONTRACT: This is a match
               to either a Rural Route or a Highway Contract record,
               both of which may have associated Box Number ranges.
            -  ``S``: STREET RECORD: This is a match to a Street record
               containing a valid primary number range.
        default_address (bool):
            Indicator that a default address was found,
            but more specific addresses exists.
        error_message (str):
            Error message for USPS data retrieval. This
            is populated when USPS processing is suspended
            because of the detection of artificially created
            addresses.

            The USPS data fields might not be populated when
            this error is present.
        cass_processed (bool):
            Indicator that the request has been CASS
            processed.
    """

    standardized_address: "UspsAddress" = proto.Field(
        proto.MESSAGE,
        number=1,
        message="UspsAddress",
    )
    delivery_point_code: str = proto.Field(
        proto.STRING,
        number=2,
    )
    delivery_point_check_digit: str = proto.Field(
        proto.STRING,
        number=3,
    )
    dpv_confirmation: str = proto.Field(
        proto.STRING,
        number=4,
    )
    dpv_footnote: str = proto.Field(
        proto.STRING,
        number=5,
    )
    dpv_cmra: str = proto.Field(
        proto.STRING,
        number=6,
    )
    dpv_vacant: str = proto.Field(
        proto.STRING,
        number=7,
    )
    dpv_no_stat: str = proto.Field(
        proto.STRING,
        number=8,
    )
    carrier_route: str = proto.Field(
        proto.STRING,
        number=9,
    )
    carrier_route_indicator: str = proto.Field(
        proto.STRING,
        number=10,
    )
    ews_no_match: bool = proto.Field(
        proto.BOOL,
        number=11,
    )
    post_office_city: str = proto.Field(
        proto.STRING,
        number=12,
    )
    post_office_state: str = proto.Field(
        proto.STRING,
        number=13,
    )
    abbreviated_city: str = proto.Field(
        proto.STRING,
        number=14,
    )
    fips_county_code: str = proto.Field(
        proto.STRING,
        number=15,
    )
    county: str = proto.Field(
        proto.STRING,
        number=16,
    )
    elot_number: str = proto.Field(
        proto.STRING,
        number=17,
    )
    elot_flag: str = proto.Field(
        proto.STRING,
        number=18,
    )
    lacs_link_return_code: str = proto.Field(
        proto.STRING,
        number=19,
    )
    lacs_link_indicator: str = proto.Field(
        proto.STRING,
        number=20,
    )
    po_box_only_postal_code: bool = proto.Field(
        proto.BOOL,
        number=21,
    )
    suitelink_footnote: str = proto.Field(
        proto.STRING,
        number=22,
    )
    pmb_designator: str = proto.Field(
        proto.STRING,
        number=23,
    )
    pmb_number: str = proto.Field(
        proto.STRING,
        number=24,
    )
    address_record_type: str = proto.Field(
        proto.STRING,
        number=25,
    )
    default_address: bool = proto.Field(
        proto.BOOL,
        number=26,
    )
    error_message: str = proto.Field(
        proto.STRING,
        number=27,
    )
    cass_processed: bool = proto.Field(
        proto.BOOL,
        number=28,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
