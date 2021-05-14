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

from google.cloud.talent_v4beta1.types import common
from google.protobuf import duration_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore
from google.protobuf import wrappers_pb2  # type: ignore
from google.type import date_pb2  # type: ignore
from google.type import latlng_pb2  # type: ignore
from google.type import timeofday_pb2  # type: ignore


__protobuf__ = proto.module(
    package="google.cloud.talent.v4beta1",
    manifest={
        "JobQuery",
        "ProfileQuery",
        "LocationFilter",
        "CompensationFilter",
        "CommuteFilter",
        "JobTitleFilter",
        "SkillFilter",
        "EmployerFilter",
        "EducationFilter",
        "WorkExperienceFilter",
        "ApplicationDateFilter",
        "ApplicationOutcomeNotesFilter",
        "ApplicationJobFilter",
        "TimeFilter",
        "CandidateAvailabilityFilter",
        "AvailabilityFilter",
        "PersonNameFilter",
    },
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
            [query][google.cloud.talent.v4beta1.JobQuery.query]. For
            example, "en-US". This field helps to better interpret the
            query.

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

            If tenant id is unspecified, the default tenant is used. For
            example, "projects/foo/companies/bar".

            At most 20 company filters are allowed.
        location_filters (Sequence[google.cloud.talent_v4beta1.types.LocationFilter]):
            The location filter specifies geo-regions containing the
            jobs to search against. See
            [LocationFilter][google.cloud.talent.v4beta1.LocationFilter]
            for more information.

            If a location value isn't specified, jobs fitting the other
            search criteria are retrieved regardless of where they're
            located.

            If multiple values are specified, jobs are retrieved from
            any of the specified locations. If different values are
            specified for the
            [LocationFilter.distance_in_miles][google.cloud.talent.v4beta1.LocationFilter.distance_in_miles]
            parameter, the maximum provided distance is used for all
            locations.

            At most 5 location filters are allowed.
        job_categories (Sequence[google.cloud.talent_v4beta1.types.JobCategory]):
            The category filter specifies the categories of jobs to
            search against. See
            [JobCategory][google.cloud.talent.v4beta1.JobCategory] for
            more information.

            If a value isn't specified, jobs from any category are
            searched against.

            If multiple values are specified, jobs from any of the
            specified categories are searched against.
        commute_filter (google.cloud.talent_v4beta1.types.CommuteFilter):
            Allows filtering jobs by commute time with different travel
            methods (for example, driving or public transit).

            Note: This only works when you specify a
            [CommuteMethod][google.cloud.talent.v4beta1.CommuteMethod].
            In this case,
            [location_filters][google.cloud.talent.v4beta1.JobQuery.location_filters]
            is ignored.

            Currently we don't support sorting by commute time.
        company_display_names (Sequence[str]):
            This filter specifies the exact company
            [Company.display_name][google.cloud.talent.v4beta1.Company.display_name]
            of the jobs to search against.

            If a value isn't specified, jobs within the search results
            are associated with any company.

            If multiple values are specified, jobs within the search
            results may be associated with any of the specified
            companies.

            At most 20 company display name filters are allowed.
        compensation_filter (google.cloud.talent_v4beta1.types.CompensationFilter):
            This search filter is applied only to
            [Job.compensation_info][google.cloud.talent.v4beta1.Job.compensation_info].
            For example, if the filter is specified as "Hourly job with
            per-hour compensation > $15", only jobs meeting these
            criteria are searched. If a filter isn't defined, all open
            jobs are searched.
        custom_attribute_filter (str):
            This filter specifies a structured syntax to match against
            the
            [Job.custom_attributes][google.cloud.talent.v4beta1.Job.custom_attributes]
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
        employment_types (Sequence[google.cloud.talent_v4beta1.types.EmploymentType]):
            The employment type filter specifies the employment type of
            jobs to search against, such as
            [EmploymentType.FULL_TIME][google.cloud.talent.v4beta1.EmploymentType.FULL_TIME].

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
        publish_time_range (google.cloud.talent_v4beta1.types.TimestampRange):
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


class ProfileQuery(proto.Message):
    r"""Filters to apply when performing the search query.
    Attributes:
        query (str):
            Keywords to match any text fields of
            profiles.
            For example, "software engineer in Palo Alto".
        location_filters (Sequence[google.cloud.talent_v4beta1.types.LocationFilter]):
            The location filter specifies geo-regions containing the
            profiles to search against.

            One of
            [LocationFilter.address][google.cloud.talent.v4beta1.LocationFilter.address]
            or
            [LocationFilter.lat_lng][google.cloud.talent.v4beta1.LocationFilter.lat_lng]
            must be provided or an error is thrown. If both
            [LocationFilter.address][google.cloud.talent.v4beta1.LocationFilter.address]
            and
            [LocationFilter.lat_lng][google.cloud.talent.v4beta1.LocationFilter.lat_lng]
            are provided, an error is thrown.

            The following logic is used to determine which locations in
            the profile to filter against:

            1. All of the profile's geocoded
               [Profile.addresses][google.cloud.talent.v4beta1.Profile.addresses]
               where
               [Address.usage][google.cloud.talent.v4beta1.Address.usage]
               is PERSONAL and
               [Address.current][google.cloud.talent.v4beta1.Address.current]
               is true.

            2. If the above set of locations is empty, all of the
               profile's geocoded
               [Profile.addresses][google.cloud.talent.v4beta1.Profile.addresses]
               where
               [Address.usage][google.cloud.talent.v4beta1.Address.usage]
               is CONTACT_INFO_USAGE_UNSPECIFIED and
               [Address.current][google.cloud.talent.v4beta1.Address.current]
               is true.

            3. If the above set of locations is empty, all of the
               profile's geocoded
               [Profile.addresses][google.cloud.talent.v4beta1.Profile.addresses]
               where
               [Address.usage][google.cloud.talent.v4beta1.Address.usage]
               is PERSONAL or CONTACT_INFO_USAGE_UNSPECIFIED and
               [Address.current][google.cloud.talent.v4beta1.Address.current]
               is not set.

            This means that any profiles without any
            [Profile.addresses][google.cloud.talent.v4beta1.Profile.addresses]
            that match any of the above criteria will not be included in
            a search with location filter. Furthermore, any
            [Profile.addresses][google.cloud.talent.v4beta1.Profile.addresses]
            where
            [Address.usage][google.cloud.talent.v4beta1.Address.usage]
            is WORK or SCHOOL or where
            [Address.current][google.cloud.talent.v4beta1.Address.current]
            is false are not considered for location filter.

            If a location filter isn't specified, profiles fitting the
            other search criteria are retrieved regardless of where
            they're located.

            If
            [LocationFilter.negated][google.cloud.talent.v4beta1.LocationFilter.negated]
            is specified, the result doesn't contain profiles from that
            location.

            If
            [LocationFilter.address][google.cloud.talent.v4beta1.LocationFilter.address]
            is provided, the
            [LocationType][google.cloud.talent.v4beta1.Location.LocationType],
            center point (latitude and longitude), and radius are
            automatically detected by the Google Maps Geocoding API and
            included as well. If
            [LocationFilter.address][google.cloud.talent.v4beta1.LocationFilter.address]
            cannot be geocoded, the filter falls back to keyword search.

            If the detected
            [LocationType][google.cloud.talent.v4beta1.Location.LocationType]
            is
            [LocationType.SUB_ADMINISTRATIVE_AREA][google.cloud.talent.v4beta1.Location.LocationType.SUB_ADMINISTRATIVE_AREA],
            [LocationType.ADMINISTRATIVE_AREA][google.cloud.talent.v4beta1.Location.LocationType.ADMINISTRATIVE_AREA],
            or
            [LocationType.COUNTRY][google.cloud.talent.v4beta1.Location.LocationType.COUNTRY],
            the filter is performed against the detected location name
            (using exact text matching). Otherwise, the filter is
            performed against the detected center point and a radius of
            detected location radius +
            [LocationFilter.distance_in_miles][google.cloud.talent.v4beta1.LocationFilter.distance_in_miles].

            If
            [LocationFilter.address][google.cloud.talent.v4beta1.LocationFilter.address]
            is provided,
            [LocationFilter.distance_in_miles][google.cloud.talent.v4beta1.LocationFilter.distance_in_miles]
            is the additional radius on top of the radius of the
            location geocoded from
            [LocationFilter.address][google.cloud.talent.v4beta1.LocationFilter.address].
            If
            [LocationFilter.lat_lng][google.cloud.talent.v4beta1.LocationFilter.lat_lng]
            is provided,
            [LocationFilter.distance_in_miles][google.cloud.talent.v4beta1.LocationFilter.distance_in_miles]
            is the only radius that is used.

            [LocationFilter.distance_in_miles][google.cloud.talent.v4beta1.LocationFilter.distance_in_miles]
            is 10 by default. Note that the value of
            [LocationFilter.distance_in_miles][google.cloud.talent.v4beta1.LocationFilter.distance_in_miles]
            is 0 if it is unset, so the server does not differentiate
            [LocationFilter.distance_in_miles][google.cloud.talent.v4beta1.LocationFilter.distance_in_miles]
            that is explicitly set to 0 and
            [LocationFilter.distance_in_miles][google.cloud.talent.v4beta1.LocationFilter.distance_in_miles]
            that is not set. Which means that if
            [LocationFilter.distance_in_miles][google.cloud.talent.v4beta1.LocationFilter.distance_in_miles]
            is explicitly set to 0, the server will use the default
            value of
            [LocationFilter.distance_in_miles][google.cloud.talent.v4beta1.LocationFilter.distance_in_miles]
            which is 10. To work around this and effectively set
            [LocationFilter.distance_in_miles][google.cloud.talent.v4beta1.LocationFilter.distance_in_miles]
            to 0, we recommend setting
            [LocationFilter.distance_in_miles][google.cloud.talent.v4beta1.LocationFilter.distance_in_miles]
            to a very small decimal number (such as 0.00001).

            If
            [LocationFilter.distance_in_miles][google.cloud.talent.v4beta1.LocationFilter.distance_in_miles]
            is negative, an error is thrown.
        job_title_filters (Sequence[google.cloud.talent_v4beta1.types.JobTitleFilter]):
            Job title filter specifies job titles of profiles to match
            on.

            If a job title isn't specified, profiles with any titles are
            retrieved.

            If multiple values are specified, profiles are retrieved
            with any of the specified job titles.

            If
            [JobTitleFilter.negated][google.cloud.talent.v4beta1.JobTitleFilter.negated]
            is specified, the result won't contain profiles with the job
            titles.

            For example, search for profiles with a job title "Product
            Manager".
        employer_filters (Sequence[google.cloud.talent_v4beta1.types.EmployerFilter]):
            Employer filter specifies employers of profiles to match on.

            If an employer filter isn't specified, profiles with any
            employers are retrieved.

            If multiple employer filters are specified, profiles with
            any matching employers are retrieved.

            If
            [EmployerFilter.negated][google.cloud.talent.v4beta1.EmployerFilter.negated]
            is specified, the result won't contain profiles that match
            the employers.

            For example, search for profiles that have working
            experience at "Google LLC".
        education_filters (Sequence[google.cloud.talent_v4beta1.types.EducationFilter]):
            Education filter specifies education of profiles to match
            on.

            If an education filter isn't specified, profiles with any
            education are retrieved.

            If multiple education filters are specified, profiles that
            match any education filters are retrieved.

            If
            [EducationFilter.negated][google.cloud.talent.v4beta1.EducationFilter.negated]
            is specified, the result won't contain profiles that match
            the educations.

            For example, search for profiles with a master degree.
        skill_filters (Sequence[google.cloud.talent_v4beta1.types.SkillFilter]):
            Skill filter specifies skill of profiles to match on.

            If a skill filter isn't specified, profiles with any skills
            are retrieved.

            If multiple skill filters are specified, profiles that match
            any skill filters are retrieved.

            If
            [SkillFilter.negated][google.cloud.talent.v4beta1.SkillFilter.negated]
            is specified, the result won't contain profiles that match
            the skills.

            For example, search for profiles that have "Java" and
            "Python" in skill list.
        work_experience_filter (Sequence[google.cloud.talent_v4beta1.types.WorkExperienceFilter]):
            Work experience filter specifies the total
            working experience of profiles to match on.

            If a work experience filter isn't specified,
            profiles with any professional experience are
            retrieved.

            If multiple work experience filters are
            specified, profiles that match any work
            experience filters are retrieved.

            For example, search for profiles with 10 years
            of work experience.
        time_filters (Sequence[google.cloud.talent_v4beta1.types.TimeFilter]):
            Time filter specifies the create/update
            timestamp of the profiles to match on.

            For example, search for profiles created since
            "2018-1-1".
        hirable_filter (google.protobuf.wrappers_pb2.BoolValue):
            The hirable filter specifies the profile's
            hirable status to match on.
        application_date_filters (Sequence[google.cloud.talent_v4beta1.types.ApplicationDateFilter]):
            The application date filters specify
            application date ranges to match on.
        application_outcome_notes_filters (Sequence[google.cloud.talent_v4beta1.types.ApplicationOutcomeNotesFilter]):
            The application outcome notes filters specify
            the notes for the outcome of the job
            application.
        application_job_filters (Sequence[google.cloud.talent_v4beta1.types.ApplicationJobFilter]):
            The application job filters specify the job
            applied for in the application.
        custom_attribute_filter (str):
            This filter specifies a structured syntax to match against
            the
            [Profile.custom_attributes][google.cloud.talent.v4beta1.Profile.custom_attributes]
            that are marked as ``filterable``.

            The syntax for this expression is a subset of Google SQL
            syntax.

            String custom attributes: supported operators are =, !=
            where the left of the operator is a custom field key and the
            right of the operator is a string (surrounded by quotes)
            value.

            Numeric custom attributes: Supported operators are '>', '<'
            or '=' operators where the left of the operator is a custom
            field key and the right of the operator is a numeric value.

            Supported functions are LOWER(<field_name>) to perform case
            insensitive match and EMPTY(<field_name>) to filter on the
            existence of a key.

            Boolean expressions (AND/OR/NOT) are supported up to 3
            levels of nesting (for example "((A AND B AND C) OR NOT D)
            AND E"), and there can be a maximum of 50
            comparisons/functions in the expression. The expression must
            be < 2000 characters in length.

            Sample Query: (key1 = "TEST" OR LOWER(key1)="test" OR NOT
            EMPTY(key1))
        candidate_availability_filter (google.cloud.talent_v4beta1.types.CandidateAvailabilityFilter):
            Deprecated. Use availability_filters instead.

            The candidate availability filter which filters based on
            availability signals.

            Signal 1: Number of days since most recent job application.
            See
            [Availability.JobApplicationAvailabilitySignal][google.cloud.talent.v4beta1.Availability.JobApplicationAvailabilitySignal]
            for the details of this signal.

            Signal 2: Number of days since last profile update. See
            [Availability.ProfileUpdateAvailabilitySignal][google.cloud.talent.v4beta1.Availability.ProfileUpdateAvailabilitySignal]
            for the details of this signal.

            The candidate availability filter helps a recruiter
            understand if a specific candidate is likely to be actively
            seeking new job opportunities based on an aggregated set of
            signals. Specifically, the intent is NOT to indicate the
            candidate's potential qualification / interest / close
            ability for a specific job.
        availability_filters (Sequence[google.cloud.talent_v4beta1.types.AvailabilityFilter]):
            The availability filter which filters based on
            [Profile.availability_signals][google.cloud.talent.v4beta1.Profile.availability_signals].

            The availability filter helps a recruiter understand if a
            specific candidate is likely to be actively seeking new job
            opportunities based on an aggregated set of signals.
            Specifically, the intent is NOT to indicate the candidate's
            potential qualification / interest / close ability for a
            specific job.

            There can be at most one
            [AvailabilityFilter][google.cloud.talent.v4beta1.AvailabilityFilter]
            per
            [signal_type][google.cloud.talent.v4beta1.AvailabilityFilter.signal_type].
            If there are multiple
            [AvailabilityFilter][google.cloud.talent.v4beta1.AvailabilityFilter]
            for a
            [signal_type][google.cloud.talent.v4beta1.AvailabilityFilter.signal_type],
            an error is thrown.
        person_name_filters (Sequence[google.cloud.talent_v4beta1.types.PersonNameFilter]):
            Person name filter specifies person name of
            profiles to match on.
            If multiple person name filters are specified,
            profiles that match any person name filters are
            retrieved.

            For example, search for profiles of candidates
            with name "John Smith".
    """

    query = proto.Field(proto.STRING, number=1,)
    location_filters = proto.RepeatedField(
        proto.MESSAGE, number=2, message="LocationFilter",
    )
    job_title_filters = proto.RepeatedField(
        proto.MESSAGE, number=3, message="JobTitleFilter",
    )
    employer_filters = proto.RepeatedField(
        proto.MESSAGE, number=4, message="EmployerFilter",
    )
    education_filters = proto.RepeatedField(
        proto.MESSAGE, number=5, message="EducationFilter",
    )
    skill_filters = proto.RepeatedField(proto.MESSAGE, number=6, message="SkillFilter",)
    work_experience_filter = proto.RepeatedField(
        proto.MESSAGE, number=7, message="WorkExperienceFilter",
    )
    time_filters = proto.RepeatedField(proto.MESSAGE, number=8, message="TimeFilter",)
    hirable_filter = proto.Field(
        proto.MESSAGE, number=9, message=wrappers_pb2.BoolValue,
    )
    application_date_filters = proto.RepeatedField(
        proto.MESSAGE, number=10, message="ApplicationDateFilter",
    )
    application_outcome_notes_filters = proto.RepeatedField(
        proto.MESSAGE, number=11, message="ApplicationOutcomeNotesFilter",
    )
    application_job_filters = proto.RepeatedField(
        proto.MESSAGE, number=13, message="ApplicationJobFilter",
    )
    custom_attribute_filter = proto.Field(proto.STRING, number=15,)
    candidate_availability_filter = proto.Field(
        proto.MESSAGE, number=16, message="CandidateAvailabilityFilter",
    )
    availability_filters = proto.RepeatedField(
        proto.MESSAGE, number=18, message="AvailabilityFilter",
    )
    person_name_filters = proto.RepeatedField(
        proto.MESSAGE, number=17, message="PersonNameFilter",
    )


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
            for details. Example: "CH" for Switzerland. Note that this
            filter is not applicable for Profile Search related queries.
        lat_lng (google.type.latlng_pb2.LatLng):
            The latitude and longitude of the geographic center to
            search from. This field is ignored if ``address`` is
            provided.
        distance_in_miles (float):
            The distance_in_miles is applied when the location being
            searched for is identified as a city or smaller. This field
            is ignored if the location being searched for is a state or
            larger.
        telecommute_preference (google.cloud.talent_v4beta1.types.LocationFilter.TelecommutePreference):
            Allows the client to return jobs without a set location,
            specifically, telecommuting jobs (telecommuting is
            considered by the service as a special location.
            [Job.posting_region][google.cloud.talent.v4beta1.Job.posting_region]
            indicates if a job permits telecommuting. If this field is
            set to
            [TelecommutePreference.TELECOMMUTE_ALLOWED][google.cloud.talent.v4beta1.LocationFilter.TelecommutePreference.TELECOMMUTE_ALLOWED],
            telecommuting jobs are searched, and
            [address][google.cloud.talent.v4beta1.LocationFilter.address]
            and
            [lat_lng][google.cloud.talent.v4beta1.LocationFilter.lat_lng]
            are ignored. If not set or set to
            [TelecommutePreference.TELECOMMUTE_EXCLUDED][google.cloud.talent.v4beta1.LocationFilter.TelecommutePreference.TELECOMMUTE_EXCLUDED],
            telecommute job are not searched.

            This filter can be used by itself to search exclusively for
            telecommuting jobs, or it can be combined with another
            location filter to search for a combination of job
            locations, such as "Mountain View" or "telecommuting" jobs.
            However, when used in combination with other location
            filters, telecommuting jobs can be treated as less relevant
            than other jobs in the search response.

            This field is only used for job search requests.
        negated (bool):
            Whether to apply negation to the filter so
            profiles matching the filter are excluded.

            Currently only supported in profile search.
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
    negated = proto.Field(proto.BOOL, number=6,)


class CompensationFilter(proto.Message):
    r"""Filter on job compensation type and amount.
    Attributes:
        type_ (google.cloud.talent_v4beta1.types.CompensationFilter.FilterType):
            Required. Type of filter.
        units (Sequence[google.cloud.talent_v4beta1.types.CompensationInfo.CompensationUnit]):
            Required. Specify desired ``base compensation entry's``
            [CompensationInfo.CompensationUnit][google.cloud.talent.v4beta1.CompensationInfo.CompensationUnit].
        range_ (google.cloud.talent_v4beta1.types.CompensationInfo.CompensationRange):
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
        commute_method (google.cloud.talent_v4beta1.types.CommuteMethod):
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
        road_traffic (google.cloud.talent_v4beta1.types.CommuteFilter.RoadTraffic):
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


class JobTitleFilter(proto.Message):
    r"""Job title of the search.
    Attributes:
        job_title (str):
            Required. The job title. For example,
            "Software engineer", or "Product manager".
        negated (bool):
            Whether to apply negation to the filter so
            profiles matching the filter are excluded.
    """

    job_title = proto.Field(proto.STRING, number=1,)
    negated = proto.Field(proto.BOOL, number=2,)


class SkillFilter(proto.Message):
    r"""Skill filter of the search.
    Attributes:
        skill (str):
            Required. The skill name. For example,
            "java", "j2ee", and so on.
        negated (bool):
            Whether to apply negation to the filter so
            profiles matching the filter are excluded.
    """

    skill = proto.Field(proto.STRING, number=1,)
    negated = proto.Field(proto.BOOL, number=2,)


class EmployerFilter(proto.Message):
    r"""Employer filter of the search.
    Attributes:
        employer (str):
            Required. The name of the employer, for
            example "Google", "Alphabet".
        mode (google.cloud.talent_v4beta1.types.EmployerFilter.EmployerFilterMode):
            Define set of
            [EmploymentRecord][google.cloud.talent.v4beta1.EmploymentRecord]s
            to search against.

            Defaults to
            [EmployerFilterMode.ALL_EMPLOYMENT_RECORDS][google.cloud.talent.v4beta1.EmployerFilter.EmployerFilterMode.ALL_EMPLOYMENT_RECORDS].
        negated (bool):
            Whether to apply negation to the filter so
            profiles matching the filter is excluded.
    """

    class EmployerFilterMode(proto.Enum):
        r"""Enum indicating which set of
        [Profile.employment_records][google.cloud.talent.v4beta1.Profile.employment_records]
        to search against.
        """
        EMPLOYER_FILTER_MODE_UNSPECIFIED = 0
        ALL_EMPLOYMENT_RECORDS = 1
        CURRENT_EMPLOYMENT_RECORDS_ONLY = 2
        PAST_EMPLOYMENT_RECORDS_ONLY = 3

    employer = proto.Field(proto.STRING, number=1,)
    mode = proto.Field(proto.ENUM, number=2, enum=EmployerFilterMode,)
    negated = proto.Field(proto.BOOL, number=3,)


class EducationFilter(proto.Message):
    r"""Education filter of the search.
    Attributes:
        school (str):
            The school name. For example "MIT",
            "University of California, Berkeley".
        field_of_study (str):
            The field of study. This is to search against value provided
            in
            [Degree.fields_of_study][google.cloud.talent.v4beta1.Degree.fields_of_study].
            For example "Computer Science", "Mathematics".
        degree_type (google.cloud.talent_v4beta1.types.DegreeType):
            Education degree in ISCED code. Each value in
            degree covers a specific level of education,
            without any expansion to upper nor lower levels
            of education degree.
        negated (bool):
            Whether to apply negation to the filter so
            profiles matching the filter is excluded.
    """

    school = proto.Field(proto.STRING, number=1,)
    field_of_study = proto.Field(proto.STRING, number=2,)
    degree_type = proto.Field(proto.ENUM, number=3, enum=common.DegreeType,)
    negated = proto.Field(proto.BOOL, number=6,)


class WorkExperienceFilter(proto.Message):
    r"""Work experience filter.

    This filter is used to search for profiles with working experience
    length between
    [min_experience][google.cloud.talent.v4beta1.WorkExperienceFilter.min_experience]
    and
    [max_experience][google.cloud.talent.v4beta1.WorkExperienceFilter.max_experience].

    Attributes:
        min_experience (google.protobuf.duration_pb2.Duration):
            The minimum duration of the work experience
            (inclusive).
        max_experience (google.protobuf.duration_pb2.Duration):
            The maximum duration of the work experience
            (exclusive).
    """

    min_experience = proto.Field(
        proto.MESSAGE, number=1, message=duration_pb2.Duration,
    )
    max_experience = proto.Field(
        proto.MESSAGE, number=2, message=duration_pb2.Duration,
    )


class ApplicationDateFilter(proto.Message):
    r"""Application Date Range Filter.

    The API matches profiles with
    [Application.application_date][google.cloud.talent.v4beta1.Application.application_date]
    between start date and end date (both boundaries are inclusive). The
    filter is ignored if both
    [start_date][google.cloud.talent.v4beta1.ApplicationDateFilter.start_date]
    and
    [end_date][google.cloud.talent.v4beta1.ApplicationDateFilter.end_date]
    are missing.

    Attributes:
        start_date (google.type.date_pb2.Date):
            Start date. If it's missing, The API matches
            profiles with application date not after the end
            date.
        end_date (google.type.date_pb2.Date):
            End date. If it's missing, The API matches
            profiles with application date not before the
            start date.
    """

    start_date = proto.Field(proto.MESSAGE, number=1, message=date_pb2.Date,)
    end_date = proto.Field(proto.MESSAGE, number=2, message=date_pb2.Date,)


class ApplicationOutcomeNotesFilter(proto.Message):
    r"""Outcome Notes Filter.
    Attributes:
        outcome_notes (str):
            Required. User entered or selected outcome reason. The API
            does an exact match on the
            [Application.outcome_notes][google.cloud.talent.v4beta1.Application.outcome_notes]
            in profiles.
        negated (bool):
            If true, The API excludes all candidates with any
            [Application.outcome_notes][google.cloud.talent.v4beta1.Application.outcome_notes]
            matching the outcome reason specified in the filter.
    """

    outcome_notes = proto.Field(proto.STRING, number=1,)
    negated = proto.Field(proto.BOOL, number=2,)


class ApplicationJobFilter(proto.Message):
    r"""Filter on the job information of Application.
    Attributes:
        job_requisition_id (str):
            The job requisition id in the application. The API does an
            exact match on the
            [Job.requisition_id][google.cloud.talent.v4beta1.Job.requisition_id]
            of
            [Application.job][google.cloud.talent.v4beta1.Application.job]
            in profiles.
        job_title (str):
            The job title in the application. The API does an exact
            match on the
            [Job.title][google.cloud.talent.v4beta1.Job.title] of
            [Application.job][google.cloud.talent.v4beta1.Application.job]
            in profiles.
        negated (bool):
            If true, the API excludes all profiles with any
            [Application.job][google.cloud.talent.v4beta1.Application.job]
            matching the filters.
    """

    job_requisition_id = proto.Field(proto.STRING, number=2,)
    job_title = proto.Field(proto.STRING, number=3,)
    negated = proto.Field(proto.BOOL, number=4,)


class TimeFilter(proto.Message):
    r"""Filter on create timestamp or update timestamp of profiles.
    Attributes:
        start_time (google.protobuf.timestamp_pb2.Timestamp):
            Start timestamp, matching profiles with the
            start time. If this field missing, The API
            matches profiles with create / update timestamp
            before the end timestamp.
        end_time (google.protobuf.timestamp_pb2.Timestamp):
            End timestamp, matching profiles with the end
            time. If this field missing, The API matches
            profiles with create / update timestamp after
            the start timestamp.
        time_field (google.cloud.talent_v4beta1.types.TimeFilter.TimeField):
            Specifies which time field to filter profiles.

            Defaults to
            [TimeField.CREATE_TIME][google.cloud.talent.v4beta1.TimeFilter.TimeField.CREATE_TIME].
    """

    class TimeField(proto.Enum):
        r"""Time fields can be used in TimeFilter."""
        TIME_FIELD_UNSPECIFIED = 0
        CREATE_TIME = 1
        UPDATE_TIME = 2

    start_time = proto.Field(proto.MESSAGE, number=1, message=timestamp_pb2.Timestamp,)
    end_time = proto.Field(proto.MESSAGE, number=2, message=timestamp_pb2.Timestamp,)
    time_field = proto.Field(proto.ENUM, number=3, enum=TimeField,)


class CandidateAvailabilityFilter(proto.Message):
    r"""Deprecated. Use AvailabilityFilter instead.
    Filter on availability signals.

    Attributes:
        negated (bool):
            It is false by default. If true, API excludes
            all the potential available profiles.
    """

    negated = proto.Field(proto.BOOL, number=1,)


class AvailabilityFilter(proto.Message):
    r"""Filter on availability signals.
    Attributes:
        signal_type (google.cloud.talent_v4beta1.types.AvailabilitySignalType):
            Required. Type of signal to apply filter on.
        range_ (google.cloud.talent_v4beta1.types.TimestampRange):
            Required. Range of times to filter candidate
            signals by.
        required (bool):
            If multiple
            [AvailabilityFilter][google.cloud.talent.v4beta1.AvailabilityFilter]
            are provided, the default behavior is to OR all filters, but
            if this field is set to true, this particular
            [AvailabilityFilter][google.cloud.talent.v4beta1.AvailabilityFilter]
            will be AND'ed against other
            [AvailabilityFilter][google.cloud.talent.v4beta1.AvailabilityFilter].
    """

    signal_type = proto.Field(proto.ENUM, number=1, enum=common.AvailabilitySignalType,)
    range_ = proto.Field(proto.MESSAGE, number=2, message=common.TimestampRange,)
    required = proto.Field(proto.BOOL, number=3,)


class PersonNameFilter(proto.Message):
    r"""Filter on person name.
    Attributes:
        person_name (str):
            Required. The person name. For example, "John Smith".

            Can be any combination of
            [PersonName.structured_name.given_name][],
            [PersonName.structured_name.middle_initial][],
            [PersonName.structured_name.family_name][], and
            [PersonName.formatted_name][google.cloud.talent.v4beta1.PersonName.formatted_name].
    """

    person_name = proto.Field(proto.STRING, number=1,)


__all__ = tuple(sorted(__protobuf__.manifest))
