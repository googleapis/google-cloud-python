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

from google.protobuf import timestamp_pb2  # type: ignore
from google.protobuf import wrappers_pb2  # type: ignore
from google.type import date_pb2  # type: ignore
from google.type import latlng_pb2  # type: ignore
from google.type import money_pb2  # type: ignore
from google.type import postal_address_pb2  # type: ignore


__protobuf__ = proto.module(
    package="google.cloud.talent.v4beta1",
    manifest={
        "CompanySize",
        "JobBenefit",
        "DegreeType",
        "EmploymentType",
        "JobLevel",
        "JobCategory",
        "PostingRegion",
        "Visibility",
        "ContactInfoUsage",
        "HtmlSanitization",
        "CommuteMethod",
        "SkillProficiencyLevel",
        "Outcome",
        "AvailabilitySignalType",
        "TimestampRange",
        "Location",
        "RequestMetadata",
        "ResponseMetadata",
        "DeviceInfo",
        "CustomAttribute",
        "SpellingCorrection",
        "CompensationInfo",
        "Certification",
        "Skill",
        "Interview",
        "Rating",
        "BatchOperationMetadata",
    },
)


class CompanySize(proto.Enum):
    r"""An enum that represents the size of the company."""
    COMPANY_SIZE_UNSPECIFIED = 0
    MINI = 1
    SMALL = 2
    SMEDIUM = 3
    MEDIUM = 4
    BIG = 5
    BIGGER = 6
    GIANT = 7


class JobBenefit(proto.Enum):
    r"""An enum that represents employee benefits included with the
    job.
    """
    JOB_BENEFIT_UNSPECIFIED = 0
    CHILD_CARE = 1
    DENTAL = 2
    DOMESTIC_PARTNER = 3
    FLEXIBLE_HOURS = 4
    MEDICAL = 5
    LIFE_INSURANCE = 6
    PARENTAL_LEAVE = 7
    RETIREMENT_PLAN = 8
    SICK_DAYS = 9
    VACATION = 10
    VISION = 11


class DegreeType(proto.Enum):
    r"""Educational degree level defined in International Standard
    Classification of Education (ISCED).
    """
    DEGREE_TYPE_UNSPECIFIED = 0
    PRIMARY_EDUCATION = 1
    LOWER_SECONDARY_EDUCATION = 2
    UPPER_SECONDARY_EDUCATION = 3
    ADULT_REMEDIAL_EDUCATION = 4
    ASSOCIATES_OR_EQUIVALENT = 5
    BACHELORS_OR_EQUIVALENT = 6
    MASTERS_OR_EQUIVALENT = 7
    DOCTORAL_OR_EQUIVALENT = 8


class EmploymentType(proto.Enum):
    r"""An enum that represents the employment type of a job."""
    EMPLOYMENT_TYPE_UNSPECIFIED = 0
    FULL_TIME = 1
    PART_TIME = 2
    CONTRACTOR = 3
    CONTRACT_TO_HIRE = 4
    TEMPORARY = 5
    INTERN = 6
    VOLUNTEER = 7
    PER_DIEM = 8
    FLY_IN_FLY_OUT = 9
    OTHER_EMPLOYMENT_TYPE = 10


class JobLevel(proto.Enum):
    r"""An enum that represents the required experience level
    required for the job.
    """
    JOB_LEVEL_UNSPECIFIED = 0
    ENTRY_LEVEL = 1
    EXPERIENCED = 2
    MANAGER = 3
    DIRECTOR = 4
    EXECUTIVE = 5


class JobCategory(proto.Enum):
    r"""An enum that represents the categorization or primary focus
    of specific role. This value is different than the "industry"
    associated with a role, which is related to the categorization
    of the company listing the job.
    """
    JOB_CATEGORY_UNSPECIFIED = 0
    ACCOUNTING_AND_FINANCE = 1
    ADMINISTRATIVE_AND_OFFICE = 2
    ADVERTISING_AND_MARKETING = 3
    ANIMAL_CARE = 4
    ART_FASHION_AND_DESIGN = 5
    BUSINESS_OPERATIONS = 6
    CLEANING_AND_FACILITIES = 7
    COMPUTER_AND_IT = 8
    CONSTRUCTION = 9
    CUSTOMER_SERVICE = 10
    EDUCATION = 11
    ENTERTAINMENT_AND_TRAVEL = 12
    FARMING_AND_OUTDOORS = 13
    HEALTHCARE = 14
    HUMAN_RESOURCES = 15
    INSTALLATION_MAINTENANCE_AND_REPAIR = 16
    LEGAL = 17
    MANAGEMENT = 18
    MANUFACTURING_AND_WAREHOUSE = 19
    MEDIA_COMMUNICATIONS_AND_WRITING = 20
    OIL_GAS_AND_MINING = 21
    PERSONAL_CARE_AND_SERVICES = 22
    PROTECTIVE_SERVICES = 23
    REAL_ESTATE = 24
    RESTAURANT_AND_HOSPITALITY = 25
    SALES_AND_RETAIL = 26
    SCIENCE_AND_ENGINEERING = 27
    SOCIAL_SERVICES_AND_NON_PROFIT = 28
    SPORTS_FITNESS_AND_RECREATION = 29
    TRANSPORTATION_AND_LOGISTICS = 30


class PostingRegion(proto.Enum):
    r"""An enum that represents the job posting region. In most
    cases, job postings don't need to specify a region. If a region
    is given, jobs are eligible for searches in the specified
    region.
    """
    POSTING_REGION_UNSPECIFIED = 0
    ADMINISTRATIVE_AREA = 1
    NATION = 2
    TELECOMMUTE = 3


class Visibility(proto.Enum):
    r"""Deprecated. All resources are only visible to the owner.
    An enum that represents who has view access to the resource.
    """
    _pb_options = {"deprecated": True}
    VISIBILITY_UNSPECIFIED = 0
    ACCOUNT_ONLY = 1
    SHARED_WITH_GOOGLE = 2
    SHARED_WITH_PUBLIC = 3


class ContactInfoUsage(proto.Enum):
    r"""Enum that represents the usage of the contact information."""
    CONTACT_INFO_USAGE_UNSPECIFIED = 0
    PERSONAL = 1
    WORK = 2
    SCHOOL = 3


class HtmlSanitization(proto.Enum):
    r"""Option for HTML content sanitization on user input fields,
    for example, job description. By setting this option, user can
    determine whether and how sanitization is performed on these
    fields.
    """
    HTML_SANITIZATION_UNSPECIFIED = 0
    HTML_SANITIZATION_DISABLED = 1
    SIMPLE_FORMATTING_ONLY = 2


class CommuteMethod(proto.Enum):
    r"""Method for commute."""
    COMMUTE_METHOD_UNSPECIFIED = 0
    DRIVING = 1
    TRANSIT = 2
    WALKING = 3
    CYCLING = 4


class SkillProficiencyLevel(proto.Enum):
    r"""Enum that represents the skill proficiency level."""
    SKILL_PROFICIENCY_LEVEL_UNSPECIFIED = 0
    UNSKILLED = 6
    FUNDAMENTAL_AWARENESS = 1
    NOVICE = 2
    INTERMEDIATE = 3
    ADVANCED = 4
    EXPERT = 5


class Outcome(proto.Enum):
    r"""The overall outcome /decision / result indicator."""
    OUTCOME_UNSPECIFIED = 0
    POSITIVE = 1
    NEUTRAL = 2
    NEGATIVE = 3
    OUTCOME_NOT_AVAILABLE = 4


class AvailabilitySignalType(proto.Enum):
    r"""The type of candidate availability signal."""
    AVAILABILITY_SIGNAL_TYPE_UNSPECIFIED = 0
    JOB_APPLICATION = 1
    RESUME_UPDATE = 2
    CANDIDATE_UPDATE = 3
    CLIENT_SUBMISSION = 4


class TimestampRange(proto.Message):
    r"""Message representing a period of time between two timestamps.
    Attributes:
        start_time (google.protobuf.timestamp_pb2.Timestamp):
            Begin of the period (inclusive).
        end_time (google.protobuf.timestamp_pb2.Timestamp):
            End of the period (exclusive).
    """

    start_time = proto.Field(proto.MESSAGE, number=1, message=timestamp_pb2.Timestamp,)
    end_time = proto.Field(proto.MESSAGE, number=2, message=timestamp_pb2.Timestamp,)


class Location(proto.Message):
    r"""A resource that represents a location with full geographic
    information.

    Attributes:
        location_type (google.cloud.talent_v4beta1.types.Location.LocationType):
            The type of a location, which corresponds to the address
            lines field of
            [google.type.PostalAddress][google.type.PostalAddress]. For
            example, "Downtown, Atlanta, GA, USA" has a type of
            [LocationType.NEIGHBORHOOD][google.cloud.talent.v4beta1.Location.LocationType.NEIGHBORHOOD],
            and "Kansas City, KS, USA" has a type of
            [LocationType.LOCALITY][google.cloud.talent.v4beta1.Location.LocationType.LOCALITY].
        postal_address (google.type.postal_address_pb2.PostalAddress):
            Postal address of the location that includes
            human readable information, such as postal
            delivery and payments addresses. Given a postal
            address, a postal service can deliver items to a
            premises, P.O. Box, or other delivery location.
        lat_lng (google.type.latlng_pb2.LatLng):
            An object representing a latitude/longitude
            pair.
        radius_miles (float):
            Radius in miles of the job location. This value is derived
            from the location bounding box in which a circle with the
            specified radius centered from
            [google.type.LatLng][google.type.LatLng] covers the area
            associated with the job location. For example, currently,
            "Mountain View, CA, USA" has a radius of 6.17 miles.
    """

    class LocationType(proto.Enum):
        r"""An enum which represents the type of a location."""
        LOCATION_TYPE_UNSPECIFIED = 0
        COUNTRY = 1
        ADMINISTRATIVE_AREA = 2
        SUB_ADMINISTRATIVE_AREA = 3
        LOCALITY = 4
        POSTAL_CODE = 5
        SUB_LOCALITY = 6
        SUB_LOCALITY_1 = 7
        SUB_LOCALITY_2 = 8
        NEIGHBORHOOD = 9
        STREET_ADDRESS = 10

    location_type = proto.Field(proto.ENUM, number=1, enum=LocationType,)
    postal_address = proto.Field(
        proto.MESSAGE, number=2, message=postal_address_pb2.PostalAddress,
    )
    lat_lng = proto.Field(proto.MESSAGE, number=3, message=latlng_pb2.LatLng,)
    radius_miles = proto.Field(proto.DOUBLE, number=4,)


class RequestMetadata(proto.Message):
    r"""Meta information related to the job searcher or entity
    conducting the job search. This information is used to improve
    the performance of the service.

    Attributes:
        domain (str):
            Required if
            [allow_missing_ids][google.cloud.talent.v4beta1.RequestMetadata.allow_missing_ids]
            is unset or ``false``.

            The client-defined scope or source of the service call,
            which typically is the domain on which the service has been
            implemented and is currently being run.

            For example, if the service is being run by client Foo,
            Inc., on job board www.foo.com and career site www.bar.com,
            then this field is set to "foo.com" for use on the job
            board, and "bar.com" for use on the career site.

            Note that any improvements to the model for a particular
            tenant site rely on this field being set correctly to a
            unique domain.

            The maximum number of allowed characters is 255.
        session_id (str):
            Required if
            [allow_missing_ids][google.cloud.talent.v4beta1.RequestMetadata.allow_missing_ids]
            is unset or ``false``.

            A unique session identification string. A session is defined
            as the duration of an end user's interaction with the
            service over a certain period. Obfuscate this field for
            privacy concerns before providing it to the service.

            Note that any improvements to the model for a particular
            tenant site rely on this field being set correctly to a
            unique session ID.

            The maximum number of allowed characters is 255.
        user_id (str):
            Required if
            [allow_missing_ids][google.cloud.talent.v4beta1.RequestMetadata.allow_missing_ids]
            is unset or ``false``.

            A unique user identification string, as determined by the
            client. To have the strongest positive impact on search
            quality make sure the client-level is unique. Obfuscate this
            field for privacy concerns before providing it to the
            service.

            Note that any improvements to the model for a particular
            tenant site rely on this field being set correctly to a
            unique user ID.

            The maximum number of allowed characters is 255.
        allow_missing_ids (bool):
            Only set when any of
            [domain][google.cloud.talent.v4beta1.RequestMetadata.domain],
            [session_id][google.cloud.talent.v4beta1.RequestMetadata.session_id]
            and
            [user_id][google.cloud.talent.v4beta1.RequestMetadata.user_id]
            isn't available for some reason. It is highly recommended
            not to set this field and provide accurate
            [domain][google.cloud.talent.v4beta1.RequestMetadata.domain],
            [session_id][google.cloud.talent.v4beta1.RequestMetadata.session_id]
            and
            [user_id][google.cloud.talent.v4beta1.RequestMetadata.user_id]
            for the best service experience.
        device_info (google.cloud.talent_v4beta1.types.DeviceInfo):
            The type of device used by the job seeker at
            the time of the call to the service.
    """

    domain = proto.Field(proto.STRING, number=1,)
    session_id = proto.Field(proto.STRING, number=2,)
    user_id = proto.Field(proto.STRING, number=3,)
    allow_missing_ids = proto.Field(proto.BOOL, number=4,)
    device_info = proto.Field(proto.MESSAGE, number=5, message="DeviceInfo",)


class ResponseMetadata(proto.Message):
    r"""Additional information returned to client, such as debugging
    information.

    Attributes:
        request_id (str):
            A unique id associated with this call.
            This id is logged for tracking purposes.
    """

    request_id = proto.Field(proto.STRING, number=1,)


class DeviceInfo(proto.Message):
    r"""Device information collected from the job seeker, candidate,
    or other entity conducting the job search. Providing this
    information improves the quality of the search results across
    devices.

    Attributes:
        device_type (google.cloud.talent_v4beta1.types.DeviceInfo.DeviceType):
            Type of the device.
        id (str):
            A device-specific ID. The ID must be a unique
            identifier that distinguishes the device from
            other devices.
    """

    class DeviceType(proto.Enum):
        r"""An enumeration describing an API access portal and exposure
        mechanism.
        """
        DEVICE_TYPE_UNSPECIFIED = 0
        WEB = 1
        MOBILE_WEB = 2
        ANDROID = 3
        IOS = 4
        BOT = 5
        OTHER = 6

    device_type = proto.Field(proto.ENUM, number=1, enum=DeviceType,)
    id = proto.Field(proto.STRING, number=2,)


class CustomAttribute(proto.Message):
    r"""Custom attribute values that are either filterable or non-
    ilterable.

    Attributes:
        string_values (Sequence[str]):
            Exactly one of
            [string_values][google.cloud.talent.v4beta1.CustomAttribute.string_values]
            or
            [long_values][google.cloud.talent.v4beta1.CustomAttribute.long_values]
            must be specified.

            This field is used to perform a string match
            (``CASE_SENSITIVE_MATCH`` or ``CASE_INSENSITIVE_MATCH``)
            search. For filterable ``string_value``\ s, a maximum total
            number of 200 values is allowed, with each ``string_value``
            has a byte size of no more than 500B. For unfilterable
            ``string_values``, the maximum total byte size of
            unfilterable ``string_values`` is 50KB.

            Empty string isn't allowed.
        long_values (Sequence[int]):
            Exactly one of
            [string_values][google.cloud.talent.v4beta1.CustomAttribute.string_values]
            or
            [long_values][google.cloud.talent.v4beta1.CustomAttribute.long_values]
            must be specified.

            This field is used to perform number range search. (``EQ``,
            ``GT``, ``GE``, ``LE``, ``LT``) over filterable
            ``long_value``.

            Currently at most 1
            [long_values][google.cloud.talent.v4beta1.CustomAttribute.long_values]
            is supported.
        filterable (bool):
            If the ``filterable`` flag is true, custom field values are
            searchable. If false, values are not searchable.

            Default is false.
    """

    string_values = proto.RepeatedField(proto.STRING, number=1,)
    long_values = proto.RepeatedField(proto.INT64, number=2,)
    filterable = proto.Field(proto.BOOL, number=3,)


class SpellingCorrection(proto.Message):
    r"""Spell check result.
    Attributes:
        corrected (bool):
            Indicates if the query was corrected by the
            spell checker.
        corrected_text (str):
            Correction output consisting of the corrected
            keyword string.
        corrected_html (str):
            Corrected output with html tags to highlight
            the corrected words. Corrected words are called
            out with the "<b><i>...</i></b>" html tags.
            For example, the user input query is "software
            enginear", where the second word, "enginear," is
            incorrect. It should be "engineer". When
            spelling correction is enabled, this value is
            "software <b><i>engineer</i></b>".
    """

    corrected = proto.Field(proto.BOOL, number=1,)
    corrected_text = proto.Field(proto.STRING, number=2,)
    corrected_html = proto.Field(proto.STRING, number=3,)


class CompensationInfo(proto.Message):
    r"""Job compensation details.
    Attributes:
        entries (Sequence[google.cloud.talent_v4beta1.types.CompensationInfo.CompensationEntry]):
            Job compensation information.

            At most one entry can be of type
            [CompensationInfo.CompensationType.BASE][google.cloud.talent.v4beta1.CompensationInfo.CompensationType.BASE],
            which is referred as **base compensation entry** for the
            job.
        annualized_base_compensation_range (google.cloud.talent_v4beta1.types.CompensationInfo.CompensationRange):
            Output only. Annualized base compensation range. Computed as
            base compensation entry's
            [CompensationEntry.amount][google.cloud.talent.v4beta1.CompensationInfo.CompensationEntry.amount]
            times
            [CompensationEntry.expected_units_per_year][google.cloud.talent.v4beta1.CompensationInfo.CompensationEntry.expected_units_per_year].

            See
            [CompensationEntry][google.cloud.talent.v4beta1.CompensationInfo.CompensationEntry]
            for explanation on compensation annualization.
        annualized_total_compensation_range (google.cloud.talent_v4beta1.types.CompensationInfo.CompensationRange):
            Output only. Annualized total compensation range. Computed
            as all compensation entries'
            [CompensationEntry.amount][google.cloud.talent.v4beta1.CompensationInfo.CompensationEntry.amount]
            times
            [CompensationEntry.expected_units_per_year][google.cloud.talent.v4beta1.CompensationInfo.CompensationEntry.expected_units_per_year].

            See
            [CompensationEntry][google.cloud.talent.v4beta1.CompensationInfo.CompensationEntry]
            for explanation on compensation annualization.
    """

    class CompensationType(proto.Enum):
        r"""The type of compensation.

        For compensation amounts specified in non-monetary amounts, describe
        the compensation scheme in the
        [CompensationEntry.description][google.cloud.talent.v4beta1.CompensationInfo.CompensationEntry.description].

        For example, tipping format is described in
        [CompensationEntry.description][google.cloud.talent.v4beta1.CompensationInfo.CompensationEntry.description]
        (for example, "expect 15-20% tips based on customer bill.") and an
        estimate of the tips provided in
        [CompensationEntry.amount][google.cloud.talent.v4beta1.CompensationInfo.CompensationEntry.amount]
        or
        [CompensationEntry.range][google.cloud.talent.v4beta1.CompensationInfo.CompensationEntry.range]
        ($10 per hour).

        For example, equity is described in
        [CompensationEntry.description][google.cloud.talent.v4beta1.CompensationInfo.CompensationEntry.description]
        (for example, "1% - 2% equity vesting over 4 years, 1 year cliff")
        and value estimated in
        [CompensationEntry.amount][google.cloud.talent.v4beta1.CompensationInfo.CompensationEntry.amount]
        or
        [CompensationEntry.range][google.cloud.talent.v4beta1.CompensationInfo.CompensationEntry.range].
        If no value estimate is possible, units are
        [CompensationUnit.COMPENSATION_UNIT_UNSPECIFIED][google.cloud.talent.v4beta1.CompensationInfo.CompensationUnit.COMPENSATION_UNIT_UNSPECIFIED]
        and then further clarified in
        [CompensationEntry.description][google.cloud.talent.v4beta1.CompensationInfo.CompensationEntry.description]
        field.
        """
        COMPENSATION_TYPE_UNSPECIFIED = 0
        BASE = 1
        BONUS = 2
        SIGNING_BONUS = 3
        EQUITY = 4
        PROFIT_SHARING = 5
        COMMISSIONS = 6
        TIPS = 7
        OTHER_COMPENSATION_TYPE = 8

    class CompensationUnit(proto.Enum):
        r"""Pay frequency."""
        COMPENSATION_UNIT_UNSPECIFIED = 0
        HOURLY = 1
        DAILY = 2
        WEEKLY = 3
        MONTHLY = 4
        YEARLY = 5
        ONE_TIME = 6
        OTHER_COMPENSATION_UNIT = 7

    class CompensationEntry(proto.Message):
        r"""A compensation entry that represents one component of compensation,
        such as base pay, bonus, or other compensation type.

        Annualization: One compensation entry can be annualized if

        -  it contains valid
           [amount][google.cloud.talent.v4beta1.CompensationInfo.CompensationEntry.amount]
           or
           [range][google.cloud.talent.v4beta1.CompensationInfo.CompensationEntry.range].
        -  and its
           [expected_units_per_year][google.cloud.talent.v4beta1.CompensationInfo.CompensationEntry.expected_units_per_year]
           is set or can be derived. Its annualized range is determined as
           ([amount][google.cloud.talent.v4beta1.CompensationInfo.CompensationEntry.amount]
           or
           [range][google.cloud.talent.v4beta1.CompensationInfo.CompensationEntry.range])
           times
           [expected_units_per_year][google.cloud.talent.v4beta1.CompensationInfo.CompensationEntry.expected_units_per_year].

        Attributes:
            type_ (google.cloud.talent_v4beta1.types.CompensationInfo.CompensationType):
                Compensation type.

                Default is
                [CompensationType.COMPENSATION_TYPE_UNSPECIFIED][google.cloud.talent.v4beta1.CompensationInfo.CompensationType.COMPENSATION_TYPE_UNSPECIFIED].
            unit (google.cloud.talent_v4beta1.types.CompensationInfo.CompensationUnit):
                Frequency of the specified amount.

                Default is
                [CompensationUnit.COMPENSATION_UNIT_UNSPECIFIED][google.cloud.talent.v4beta1.CompensationInfo.CompensationUnit.COMPENSATION_UNIT_UNSPECIFIED].
            amount (google.type.money_pb2.Money):
                Compensation amount.
            range_ (google.cloud.talent_v4beta1.types.CompensationInfo.CompensationRange):
                Compensation range.
            description (str):
                Compensation description.  For example, could
                indicate equity terms or provide additional
                context to an estimated bonus.
            expected_units_per_year (google.protobuf.wrappers_pb2.DoubleValue):
                Expected number of units paid each year. If not specified,
                when
                [Job.employment_types][google.cloud.talent.v4beta1.Job.employment_types]
                is FULLTIME, a default value is inferred based on
                [unit][google.cloud.talent.v4beta1.CompensationInfo.CompensationEntry.unit].
                Default values:

                -  HOURLY: 2080
                -  DAILY: 260
                -  WEEKLY: 52
                -  MONTHLY: 12
                -  ANNUAL: 1
        """

        type_ = proto.Field(
            proto.ENUM, number=1, enum="CompensationInfo.CompensationType",
        )
        unit = proto.Field(
            proto.ENUM, number=2, enum="CompensationInfo.CompensationUnit",
        )
        amount = proto.Field(
            proto.MESSAGE,
            number=3,
            oneof="compensation_amount",
            message=money_pb2.Money,
        )
        range_ = proto.Field(
            proto.MESSAGE,
            number=4,
            oneof="compensation_amount",
            message="CompensationInfo.CompensationRange",
        )
        description = proto.Field(proto.STRING, number=5,)
        expected_units_per_year = proto.Field(
            proto.MESSAGE, number=6, message=wrappers_pb2.DoubleValue,
        )

    class CompensationRange(proto.Message):
        r"""Compensation range.
        Attributes:
            max_compensation (google.type.money_pb2.Money):
                The maximum amount of compensation. If left empty, the value
                is set to a maximal compensation value and the currency code
                is set to match the [currency
                code][google.type.Money.currency_code] of min_compensation.
            min_compensation (google.type.money_pb2.Money):
                The minimum amount of compensation. If left empty, the value
                is set to zero and the currency code is set to match the
                [currency code][google.type.Money.currency_code] of
                max_compensation.
        """

        max_compensation = proto.Field(
            proto.MESSAGE, number=2, message=money_pb2.Money,
        )
        min_compensation = proto.Field(
            proto.MESSAGE, number=1, message=money_pb2.Money,
        )

    entries = proto.RepeatedField(proto.MESSAGE, number=1, message=CompensationEntry,)
    annualized_base_compensation_range = proto.Field(
        proto.MESSAGE, number=2, message=CompensationRange,
    )
    annualized_total_compensation_range = proto.Field(
        proto.MESSAGE, number=3, message=CompensationRange,
    )


class Certification(proto.Message):
    r"""Resource that represents a license or certification.
    Attributes:
        display_name (str):
            Name of license or certification.
            Number of characters allowed is 100.
        acquire_date (google.type.date_pb2.Date):
            Acquisition date or effective date of license
            or certification.
        expire_date (google.type.date_pb2.Date):
            Expiration date of license of certification.
        authority (str):
            Authority of license, such as government.
            Number of characters allowed is 100.
        description (str):
            Description of license or certification.
            Number of characters allowed is 100,000.
    """

    display_name = proto.Field(proto.STRING, number=1,)
    acquire_date = proto.Field(proto.MESSAGE, number=2, message=date_pb2.Date,)
    expire_date = proto.Field(proto.MESSAGE, number=3, message=date_pb2.Date,)
    authority = proto.Field(proto.STRING, number=4,)
    description = proto.Field(proto.STRING, number=5,)


class Skill(proto.Message):
    r"""Resource that represents a skill of a candidate.
    Attributes:
        display_name (str):
            Skill display name.
            For example, "Java", "Python".

            Number of characters allowed is 100.
        last_used_date (google.type.date_pb2.Date):
            The last time this skill was used.
        level (google.cloud.talent_v4beta1.types.SkillProficiencyLevel):
            Skill proficiency level which indicates how
            proficient the candidate is at this skill.
        context (str):
            A paragraph describes context of this skill.
            Number of characters allowed is 100,000.
        skill_name_snippet (str):
            Output only. Skill name snippet shows how the
            [display_name][google.cloud.talent.v4beta1.Skill.display_name]
            is related to a search query. It's empty if the
            [display_name][google.cloud.talent.v4beta1.Skill.display_name]
            isn't related to the search query.
    """

    display_name = proto.Field(proto.STRING, number=1,)
    last_used_date = proto.Field(proto.MESSAGE, number=2, message=date_pb2.Date,)
    level = proto.Field(proto.ENUM, number=3, enum="SkillProficiencyLevel",)
    context = proto.Field(proto.STRING, number=4,)
    skill_name_snippet = proto.Field(proto.STRING, number=5,)


class Interview(proto.Message):
    r"""Details of an interview.
    Attributes:
        rating (google.cloud.talent_v4beta1.types.Rating):
            The rating on this interview.
        outcome (google.cloud.talent_v4beta1.types.Outcome):
            Required. The overall decision resulting from
            this interview (positive, negative, nuetral).
    """

    rating = proto.Field(proto.MESSAGE, number=6, message="Rating",)
    outcome = proto.Field(proto.ENUM, number=7, enum="Outcome",)


class Rating(proto.Message):
    r"""The details of the score received for an assessment or
    interview.

    Attributes:
        overall (float):
            Overall score.
        min_ (float):
            The minimum value for the score.
        max_ (float):
            The maximum value for the score.
        interval (float):
            The steps within the score (for example,
            interval = 1 max = 5 min = 1 indicates that the
            score can be 1, 2, 3, 4, or 5)
    """

    overall = proto.Field(proto.DOUBLE, number=1,)
    min_ = proto.Field(proto.DOUBLE, number=2,)
    max_ = proto.Field(proto.DOUBLE, number=3,)
    interval = proto.Field(proto.DOUBLE, number=4,)


class BatchOperationMetadata(proto.Message):
    r"""Metadata used for long running operations returned by CTS batch
    APIs. It's used to replace
    [google.longrunning.Operation.metadata][google.longrunning.Operation.metadata].

    Attributes:
        state (google.cloud.talent_v4beta1.types.BatchOperationMetadata.State):
            The state of a long running operation.
        state_description (str):
            More detailed information about operation
            state.
        success_count (int):
            Count of successful item(s) inside an
            operation.
        failure_count (int):
            Count of failed item(s) inside an operation.
        total_count (int):
            Count of total item(s) inside an operation.
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            The time when the batch operation is created.
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            The time when the batch operation status is updated. The
            metadata and the
            [update_time][google.cloud.talent.v4beta1.BatchOperationMetadata.update_time]
            is refreshed every minute otherwise cached data is returned.
        end_time (google.protobuf.timestamp_pb2.Timestamp):
            The time when the batch operation is finished and
            [google.longrunning.Operation.done][google.longrunning.Operation.done]
            is set to ``true``.
    """

    class State(proto.Enum):
        r""""""
        STATE_UNSPECIFIED = 0
        INITIALIZING = 1
        PROCESSING = 2
        SUCCEEDED = 3
        FAILED = 4
        CANCELLING = 5
        CANCELLED = 6

    state = proto.Field(proto.ENUM, number=1, enum=State,)
    state_description = proto.Field(proto.STRING, number=2,)
    success_count = proto.Field(proto.INT32, number=3,)
    failure_count = proto.Field(proto.INT32, number=4,)
    total_count = proto.Field(proto.INT32, number=5,)
    create_time = proto.Field(proto.MESSAGE, number=6, message=timestamp_pb2.Timestamp,)
    update_time = proto.Field(proto.MESSAGE, number=7, message=timestamp_pb2.Timestamp,)
    end_time = proto.Field(proto.MESSAGE, number=8, message=timestamp_pb2.Timestamp,)


__all__ = tuple(sorted(__protobuf__.manifest))
