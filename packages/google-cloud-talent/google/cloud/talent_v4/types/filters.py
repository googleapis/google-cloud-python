# -*- coding: utf-8 -*-
# Copyright 2020 Google LLC
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
import proto  # type: ignore

from google.cloud.talent_v4.types import common
from google.protobuf import duration_pb2  # type: ignore
from google.type import latlng_pb2  # type: ignore
from google.type import timeofday_pb2  # type: ignore


__protobuf__ = proto.module(
    package="google.cloud.talent.v4",
    manifest={"JobQuery", "LocationFilter", "CompensationFilter", "CommuteFilter",},
)


class JobQuery(proto.Message):
    r"""The query required to perform a search query.
    Attributes:
        query (str):
            The query string that matches against the job
            title, description, and location fields.

            The maximum number of allowed characters is 255.
        query_language_code (str):
            The language code of
            [query][google.cloud.talent.v4.JobQuery.query]. For example,
            "en-US". This field helps to better interpret the query.

            If a value isn't specified, the query language code is
            automatically detected, which may not be accurate.

            Language code should be in BCP-47 format, such as "en-US" or
            "sr-Latn". For more information, see `Tags for Identifying
            Languages <https://tools.ietf.org/html/bcp47>`__.
        companies (Sequence[str]):
            This filter specifies the company entities to search
            against.

            If a value isn't specified, jobs are searched for against
            all companies.

            If multiple values are specified, jobs are searched against
            the companies specified.

            The format is
            "projects/{project_id}/tenants/{tenant_id}/companies/{company_id}".
            For example, "projects/foo/tenants/bar/companies/baz".

            At most 20 company filters are allowed.
        location_filters (Sequence[google.cloud.talent_v4.types.LocationFilter]):
            The location filter specifies geo-regions containing the
            jobs to search against. See
            [LocationFilter][google.cloud.talent.v4.LocationFilter] for
            more information.

            If a location value isn't specified, jobs fitting the other
            search criteria are retrieved regardless of where they're
            located.

            If multiple values are specified, jobs are retrieved from
            any of the specified locations. If different values are
            specified for the
            [LocationFilter.distance_in_miles][google.cloud.talent.v4.LocationFilter.distance_in_miles]
            parameter, the maximum provided distance is used for all
            locations.

            At most 5 location filters are allowed.
        job_categories (Sequence[google.cloud.talent_v4.types.JobCategory]):
            The category filter specifies the categories of jobs to
            search against. See
            [JobCategory][google.cloud.talent.v4.JobCategory] for more
            information.

            If a value isn't specified, jobs from any category are
            searched against.

            If multiple values are specified, jobs from any of the
            specified categories are searched against.
        commute_filter (google.cloud.talent_v4.types.CommuteFilter):
            Allows filtering jobs by commute time with different travel
            methods (for example, driving or public transit).

            Note: This only works when you specify a
            [CommuteMethod][google.cloud.talent.v4.CommuteMethod]. In
            this case,
            [location_filters][google.cloud.talent.v4.JobQuery.location_filters]
            is ignored.

            Currently we don't support sorting by commute time.
        company_display_names (Sequence[str]):
            This filter specifies the exact company
            [Company.display_name][google.cloud.talent.v4.Company.display_name]
            of the jobs to search against.

            If a value isn't specified, jobs within the search results
            are associated with any company.

            If multiple values are specified, jobs within the search
            results may be associated with any of the specified
            companies.

            At most 20 company display name filters are allowed.
        compensation_filter (google.cloud.talent_v4.types.CompensationFilter):
            This search filter is applied only to
            [Job.compensation_info][google.cloud.talent.v4.Job.compensation_info].
            For example, if the filter is specified as "Hourly job with
            per-hour compensation > $15", only jobs meeting these
            criteria are searched. If a filter isn't defined, all open
            jobs are searched.
        custom_attribute_filter (str):
            This filter specifies a structured syntax to match against
            the
            [Job.custom_attributes][google.cloud.talent.v4.Job.custom_attributes]
            marked as ``filterable``.

            The syntax for this expression is a subset of SQL syntax.

            Supported operators are: ``=``, ``!=``, ``<``, ``<=``,
            ``>``, and ``>=`` where the left of the operator is a custom
            field key and the right of the operator is a number or a
            quoted string. You must escape backslash (\) and quote (")
            characters.

            Supported functions are ``LOWER([field_name])`` to perform a
            case insensitive match and ``EMPTY([field_name])`` to filter
            on the existence of a key.

            Boolean expressions (AND/OR/NOT) are supported up to 3
            levels of nesting (for example, "((A AND B AND C) OR NOT D)
            AND E"), a maximum of 100 comparisons or functions are
            allowed in the expression. The expression must be < 6000
            bytes in length.

            Sample Query:
            ``(LOWER(driving_license)="class \"a\"" OR EMPTY(driving_license)) AND driving_years > 10``
        disable_spell_check (bool):
            This flag controls the spell-check feature.
            If false, the service attempts to correct a
            misspelled query, for example, "enginee" is
            corrected to "engineer".
            Defaults to false: a spell check is performed.
        employment_types (Sequence[google.cloud.talent_v4.types.EmploymentType]):
            The employment type filter specifies the employment type of
            jobs to search against, such as
            [EmploymentType.FULL_TIME][google.cloud.talent.v4.EmploymentType.FULL_TIME].

            If a value isn't specified, jobs in the search results
            includes any employment type.

            If multiple values are specified, jobs in the search results
            include any of the specified employment types.
        language_codes (Sequence[str]):
            This filter specifies the locale of jobs to search against,
            for example, "en-US".

            If a value isn't specified, the search results can contain
            jobs in any locale.

            Language codes should be in BCP-47 format, such as "en-US"
            or "sr-Latn". For more information, see `Tags for
            Identifying
            Languages <https://tools.ietf.org/html/bcp47>`__.

            At most 10 language code filters are allowed.
        publish_time_range (google.cloud.talent_v4.types.TimestampRange):
            Jobs published within a range specified by
            this filter are searched against.
        excluded_jobs (Sequence[str]):
            This filter specifies a list of job names to
            be excluded during search.
            At most 400 excluded job names are allowed.
    """

    query = proto.Field(proto.STRING, number=1,)
    query_language_code = proto.Field(proto.STRING, number=14,)
    companies = proto.RepeatedField(proto.STRING, number=2,)
    location_filters = proto.RepeatedField(
        proto.MESSAGE, number=3, message="LocationFilter",
    )
    job_categories = proto.RepeatedField(proto.ENUM, number=4, enum=common.JobCategory,)
    commute_filter = proto.Field(proto.MESSAGE, number=5, message="CommuteFilter",)
    company_display_names = proto.RepeatedField(proto.STRING, number=6,)
    compensation_filter = proto.Field(
        proto.MESSAGE, number=7, message="CompensationFilter",
    )
    custom_attribute_filter = proto.Field(proto.STRING, number=8,)
    disable_spell_check = proto.Field(proto.BOOL, number=9,)
    employment_types = proto.RepeatedField(
        proto.ENUM, number=10, enum=common.EmploymentType,
    )
    language_codes = proto.RepeatedField(proto.STRING, number=11,)
    publish_time_range = proto.Field(
        proto.MESSAGE, number=12, message=common.TimestampRange,
    )
    excluded_jobs = proto.RepeatedField(proto.STRING, number=13,)


class LocationFilter(proto.Message):
    r"""Geographic region of the search.
    Attributes:
        address (str):
            The address name, such as "Mountain View" or
            "Bay Area".
        region_code (str):
            CLDR region code of the country/region of the address. This
            is used to address ambiguity of the user-input location, for
            example, "Liverpool" against "Liverpool, NY, US" or
            "Liverpool, UK".

            Set this field to bias location resolution toward a specific
            country or territory. If this field is not set, application
            behavior is biased toward the United States by default.

            See
            https://www.unicode.org/cldr/charts/30/supplemental/territory_information.html
            for details. Example: "CH" for Switzerland.
        lat_lng (google.type.latlng_pb2.LatLng):
            The latitude and longitude of the geographic center to
            search from. This field is ignored if ``address`` is
            provided.
        distance_in_miles (float):
            The distance_in_miles is applied when the location being
            searched for is identified as a city or smaller. This field
            is ignored if the location being searched for is a state or
            larger.
        telecommute_preference (google.cloud.talent_v4.types.LocationFilter.TelecommutePreference):
            Allows the client to return jobs without a set location,
            specifically, telecommuting jobs (telecommuting is
            considered by the service as a special location.
            [Job.posting_region][google.cloud.talent.v4.Job.posting_region]
            indicates if a job permits telecommuting. If this field is
            set to
            [TelecommutePreference.TELECOMMUTE_ALLOWED][google.cloud.talent.v4.LocationFilter.TelecommutePreference.TELECOMMUTE_ALLOWED],
            telecommuting jobs are searched, and
            [address][google.cloud.talent.v4.LocationFilter.address] and
            [lat_lng][google.cloud.talent.v4.LocationFilter.lat_lng] are
            ignored. If not set or set to
            [TelecommutePreference.TELECOMMUTE_EXCLUDED][google.cloud.talent.v4.LocationFilter.TelecommutePreference.TELECOMMUTE_EXCLUDED],
            telecommute job are not searched.

            This filter can be used by itself to search exclusively for
            telecommuting jobs, or it can be combined with another
            location filter to search for a combination of job
            locations, such as "Mountain View" or "telecommuting" jobs.
            However, when used in combination with other location
            filters, telecommuting jobs can be treated as less relevant
            than other jobs in the search response.

            This field is only used for job search requests.
    """

    class TelecommutePreference(proto.Enum):
        r"""Specify whether to include telecommute jobs."""
        TELECOMMUTE_PREFERENCE_UNSPECIFIED = 0
        TELECOMMUTE_EXCLUDED = 1
        TELECOMMUTE_ALLOWED = 2

    address = proto.Field(proto.STRING, number=1,)
    region_code = proto.Field(proto.STRING, number=2,)
    lat_lng = proto.Field(proto.MESSAGE, number=3, message=latlng_pb2.LatLng,)
    distance_in_miles = proto.Field(proto.DOUBLE, number=4,)
    telecommute_preference = proto.Field(
        proto.ENUM, number=5, enum=TelecommutePreference,
    )


class CompensationFilter(proto.Message):
    r"""Filter on job compensation type and amount.
    Attributes:
        type_ (google.cloud.talent_v4.types.CompensationFilter.FilterType):
            Required. Type of filter.
        units (Sequence[google.cloud.talent_v4.types.CompensationInfo.CompensationUnit]):
            Required. Specify desired ``base compensation entry's``
            [CompensationInfo.CompensationUnit][google.cloud.talent.v4.CompensationInfo.CompensationUnit].
        range_ (google.cloud.talent_v4.types.CompensationInfo.CompensationRange):
            Compensation range.
        include_jobs_with_unspecified_compensation_range (bool):
            If set to true, jobs with unspecified
            compensation range fields are included.
    """

    class FilterType(proto.Enum):
        r"""Specify the type of filtering."""
        FILTER_TYPE_UNSPECIFIED = 0
        UNIT_ONLY = 1
        UNIT_AND_AMOUNT = 2
        ANNUALIZED_BASE_AMOUNT = 3
        ANNUALIZED_TOTAL_AMOUNT = 4

    type_ = proto.Field(proto.ENUM, number=1, enum=FilterType,)
    units = proto.RepeatedField(
        proto.ENUM, number=2, enum=common.CompensationInfo.CompensationUnit,
    )
    range_ = proto.Field(
        proto.MESSAGE, number=3, message=common.CompensationInfo.CompensationRange,
    )
    include_jobs_with_unspecified_compensation_range = proto.Field(
        proto.BOOL, number=4,
    )


class CommuteFilter(proto.Message):
    r"""Parameters needed for commute search.
    Attributes:
        commute_method (google.cloud.talent_v4.types.CommuteMethod):
            Required. The method of transportation to
            calculate the commute time for.
        start_coordinates (google.type.latlng_pb2.LatLng):
            Required. The latitude and longitude of the
            location to calculate the commute time from.
        travel_duration (google.protobuf.duration_pb2.Duration):
            Required. The maximum travel time in seconds. The maximum
            allowed value is ``3600s`` (one hour). Format is ``123s``.
        allow_imprecise_addresses (bool):
            If ``true``, jobs without street level addresses may also be
            returned. For city level addresses, the city center is used.
            For state and coarser level addresses, text matching is
            used. If this field is set to ``false`` or isn't specified,
            only jobs that include street level addresses will be
            returned by commute search.
        road_traffic (google.cloud.talent_v4.types.CommuteFilter.RoadTraffic):
            Specifies the traffic density to use when
            calculating commute time.
        departure_time (google.type.timeofday_pb2.TimeOfDay):
            The departure time used to calculate traffic impact,
            represented as
            [google.type.TimeOfDay][google.type.TimeOfDay] in local time
            zone.

            Currently traffic model is restricted to hour level
            resolution.
    """

    class RoadTraffic(proto.Enum):
        r"""The traffic density to use when calculating commute time."""
        ROAD_TRAFFIC_UNSPECIFIED = 0
        TRAFFIC_FREE = 1
        BUSY_HOUR = 2

    commute_method = proto.Field(proto.ENUM, number=1, enum=common.CommuteMethod,)
    start_coordinates = proto.Field(proto.MESSAGE, number=2, message=latlng_pb2.LatLng,)
    travel_duration = proto.Field(
        proto.MESSAGE, number=3, message=duration_pb2.Duration,
    )
    allow_imprecise_addresses = proto.Field(proto.BOOL, number=4,)
    road_traffic = proto.Field(
        proto.ENUM, number=5, oneof="traffic_option", enum=RoadTraffic,
    )
    departure_time = proto.Field(
        proto.MESSAGE,
        number=6,
        oneof="traffic_option",
        message=timeofday_pb2.TimeOfDay,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
