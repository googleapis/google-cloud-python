# -*- coding: utf-8 -*-
#
# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Wrappers for protocol buffer enum types."""

import enum


class CommuteMethod(enum.IntEnum):
    """
    Method for commute.

    Attributes:
      COMMUTE_METHOD_UNSPECIFIED (int): Commute method isn't specified.
      DRIVING (int): Commute time is calculated based on driving time.
      TRANSIT (int): Commute time is calculated based on public transit including bus, metro,
      subway, and so on.
      WALKING (int): Commute time is calculated based on walking time.
      CYCLING (int): Commute time is calculated based on biking time.
    """

    COMMUTE_METHOD_UNSPECIFIED = 0
    DRIVING = 1
    TRANSIT = 2
    WALKING = 3
    CYCLING = 4


class CompanySize(enum.IntEnum):
    """
    An enum that represents the size of the company.

    Attributes:
      COMPANY_SIZE_UNSPECIFIED (int): Default value if the size isn't specified.
      MINI (int): The company has less than 50 employees.
      SMALL (int): The company has between 50 and 99 employees.
      SMEDIUM (int): The company has between 100 and 499 employees.
      MEDIUM (int): The company has between 500 and 999 employees.
      BIG (int): The company has between 1,000 and 4,999 employees.
      BIGGER (int): The company has between 5,000 and 9,999 employees.
      GIANT (int): The company has 10,000 or more employees.
    """

    COMPANY_SIZE_UNSPECIFIED = 0
    MINI = 1
    SMALL = 2
    SMEDIUM = 3
    MEDIUM = 4
    BIG = 5
    BIGGER = 6
    GIANT = 7


class ContactInfoUsage(enum.IntEnum):
    """
    Enum that represents the usage of the contact information.

    Attributes:
      CONTACT_INFO_USAGE_UNSPECIFIED (int): Default value.
      PERSONAL (int): Personal use.
      WORK (int): Work use.
      SCHOOL (int): School use.
    """

    CONTACT_INFO_USAGE_UNSPECIFIED = 0
    PERSONAL = 1
    WORK = 2
    SCHOOL = 3


class DegreeType(enum.IntEnum):
    """
    Educational degree level defined in International Standard Classification
    of Education (ISCED).

    Attributes:
      DEGREE_TYPE_UNSPECIFIED (int): Default value. Represents no degree, or early childhood education.
      Maps to ISCED code 0.
      Ex) Kindergarten
      PRIMARY_EDUCATION (int): Primary education which is typically the first stage of compulsory
      education. ISCED code 1.
      Ex) Elementary school
      LOWER_SECONDARY_EDUCATION (int): Lower secondary education; First stage of secondary education building on
      primary education, typically with a more subject-oriented curriculum.
      ISCED code 2.
      Ex) Middle school
      UPPER_SECONDARY_EDUCATION (int): Middle education; Second/final stage of secondary education preparing for
      tertiary education and/or providing skills relevant to employment.
      Usually with an increased range of subject options and streams. ISCED
      code 3.
      Ex) High school
      ADULT_REMEDIAL_EDUCATION (int): Adult Remedial Education; Programmes providing learning experiences that
      build on secondary education and prepare for labour market entry and/or
      tertiary education. The content is broader than secondary but not as
      complex as tertiary education. ISCED code 4.
      ASSOCIATES_OR_EQUIVALENT (int): Associate's or equivalent; Short first tertiary programmes that are
      typically practically-based, occupationally-specific and prepare for
      labour market entry. These programmes may also provide a pathway to other
      tertiary programmes. ISCED code 5.
      BACHELORS_OR_EQUIVALENT (int): Bachelor's or equivalent; Programmes designed to provide intermediate
      academic and/or professional knowledge, skills and competencies leading
      to a first tertiary degree or equivalent qualification. ISCED code 6.
      MASTERS_OR_EQUIVALENT (int): Master's or equivalent; Programmes designed to provide advanced academic
      and/or professional knowledge, skills and competencies leading to a
      second tertiary degree or equivalent qualification. ISCED code 7.
      DOCTORAL_OR_EQUIVALENT (int): Doctoral or equivalent; Programmes designed primarily to lead to an
      advanced research qualification, usually concluding with the submission
      and defense of a substantive dissertation of publishable quality based on
      original research. ISCED code 8.
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


class EmploymentType(enum.IntEnum):
    """
    An enum that represents the employment type of a job.

    Attributes:
      EMPLOYMENT_TYPE_UNSPECIFIED (int): The default value if the employment type isn't specified.
      FULL_TIME (int): The job requires working a number of hours that constitute full
      time employment, typically 40 or more hours per week.
      PART_TIME (int): The job entails working fewer hours than a full time job,
      typically less than 40 hours a week.
      CONTRACTOR (int): The job is offered as a contracted, as opposed to a salaried employee,
      position.
      CONTRACT_TO_HIRE (int): The job is offered as a contracted position with the understanding that
      it's converted into a full-time position at the end of the contract.
      Jobs of this type are also returned by a search for
      ``EmploymentType.CONTRACTOR`` jobs.
      TEMPORARY (int): The job is offered as a temporary employment opportunity, usually
      a short-term engagement.
      INTERN (int): The job is a fixed-term opportunity for students or entry-level job
      seekers to obtain on-the-job training, typically offered as a summer
      position.
      VOLUNTEER (int): The is an opportunity for an individual to volunteer, where there's no
      expectation of compensation for the provided services.
      PER_DIEM (int): The job requires an employee to work on an as-needed basis with a
      flexible schedule.
      FLY_IN_FLY_OUT (int): The job involves employing people in remote areas and flying them
      temporarily to the work site instead of relocating employees and their
      families permanently.
      OTHER_EMPLOYMENT_TYPE (int): The job does not fit any of the other listed types.
    """

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


class HtmlSanitization(enum.IntEnum):
    """
    Input only.

    Option for HTML content sanitization on user input fields, for example, job
    description. By setting this option, user can determine whether and how
    sanitization is performed on these fields.

    Attributes:
      HTML_SANITIZATION_UNSPECIFIED (int): Default value.
      HTML_SANITIZATION_DISABLED (int): Disables sanitization on HTML input.
      SIMPLE_FORMATTING_ONLY (int): Sanitizes HTML input, only accepts bold, italic, ordered list, and
      unordered list markup tags.
    """

    HTML_SANITIZATION_UNSPECIFIED = 0
    HTML_SANITIZATION_DISABLED = 1
    SIMPLE_FORMATTING_ONLY = 2


class JobBenefit(enum.IntEnum):
    """
    An enum that represents employee benefits included with the job.

    Attributes:
      JOB_BENEFIT_UNSPECIFIED (int): Default value if the type isn't specified.
      CHILD_CARE (int): The job includes access to programs that support child care, such
      as daycare.
      DENTAL (int): The job includes dental services covered by a dental
      insurance plan.
      DOMESTIC_PARTNER (int): The job offers specific benefits to domestic partners.
      FLEXIBLE_HOURS (int): The job allows for a flexible work schedule.
      MEDICAL (int): The job includes health services covered by a medical insurance plan.
      LIFE_INSURANCE (int): The job includes a life insurance plan provided by the employer or
      available for purchase by the employee.
      PARENTAL_LEAVE (int): The job allows for a leave of absence to a parent to care for a newborn
      child.
      RETIREMENT_PLAN (int): The job includes a workplace retirement plan provided by the
      employer or available for purchase by the employee.
      SICK_DAYS (int): The job allows for paid time off due to illness.
      VACATION (int): The job includes paid time off for vacation.
      VISION (int): The job includes vision services covered by a vision
      insurance plan.
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


class JobCategory(enum.IntEnum):
    """
    An enum that represents the categorization or primary focus of specific
    role. This value is different than the "industry" associated with a role,
    which is related to the categorization of the company listing the job.

    Attributes:
      JOB_CATEGORY_UNSPECIFIED (int): The default value if the category isn't specified.
      ACCOUNTING_AND_FINANCE (int): An accounting and finance job, such as an Accountant.
      ADMINISTRATIVE_AND_OFFICE (int): An administrative and office job, such as an Administrative Assistant.
      ADVERTISING_AND_MARKETING (int): An advertising and marketing job, such as Marketing Manager.
      ANIMAL_CARE (int): An animal care job, such as Veterinarian.
      ART_FASHION_AND_DESIGN (int): An art, fashion, or design job, such as Designer.
      BUSINESS_OPERATIONS (int): A business operations job, such as Business Operations Manager.
      CLEANING_AND_FACILITIES (int): A cleaning and facilities job, such as Custodial Staff.
      COMPUTER_AND_IT (int): A computer and IT job, such as Systems Administrator.
      CONSTRUCTION (int): A construction job, such as General Laborer.
      CUSTOMER_SERVICE (int): A customer service job, such s Cashier.
      EDUCATION (int): An education job, such as School Teacher.
      ENTERTAINMENT_AND_TRAVEL (int): An entertainment and travel job, such as Flight Attendant.
      FARMING_AND_OUTDOORS (int): A farming or outdoor job, such as Park Ranger.
      HEALTHCARE (int): A healthcare job, such as Registered Nurse.
      HUMAN_RESOURCES (int): A human resources job, such as Human Resources Director.
      INSTALLATION_MAINTENANCE_AND_REPAIR (int): An installation, maintenance, or repair job, such as Electrician.
      LEGAL (int): A legal job, such as Law Clerk.
      MANAGEMENT (int): A management job, often used in conjunction with another category,
      such as Store Manager.
      MANUFACTURING_AND_WAREHOUSE (int): A manufacturing or warehouse job, such as Assembly Technician.
      MEDIA_COMMUNICATIONS_AND_WRITING (int): A media, communications, or writing job, such as Media Relations.
      OIL_GAS_AND_MINING (int): An oil, gas or mining job, such as Offshore Driller.
      PERSONAL_CARE_AND_SERVICES (int): A personal care and services job, such as Hair Stylist.
      PROTECTIVE_SERVICES (int): A protective services job, such as Security Guard.
      REAL_ESTATE (int): A real estate job, such as Buyer's Agent.
      RESTAURANT_AND_HOSPITALITY (int): A restaurant and hospitality job, such as Restaurant Server.
      SALES_AND_RETAIL (int): A sales and/or retail job, such Sales Associate.
      SCIENCE_AND_ENGINEERING (int): A science and engineering job, such as Lab Technician.
      SOCIAL_SERVICES_AND_NON_PROFIT (int): A social services or non-profit job, such as Case Worker.
      SPORTS_FITNESS_AND_RECREATION (int): A sports, fitness, or recreation job, such as Personal Trainer.
      TRANSPORTATION_AND_LOGISTICS (int): A transportation or logistics job, such as Truck Driver.
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


class JobLevel(enum.IntEnum):
    """
    An enum that represents the required experience level required for the job.

    Attributes:
      JOB_LEVEL_UNSPECIFIED (int): The default value if the level isn't specified.
      ENTRY_LEVEL (int): Entry-level individual contributors, typically with less than 2 years of
      experience in a similar role. Includes interns.
      EXPERIENCED (int): Experienced individual contributors, typically with 2+ years of
      experience in a similar role.
      MANAGER (int): Entry- to mid-level managers responsible for managing a team of people.
      DIRECTOR (int): Senior-level managers responsible for managing teams of managers.
      EXECUTIVE (int): Executive-level managers and above, including C-level positions.
    """

    JOB_LEVEL_UNSPECIFIED = 0
    ENTRY_LEVEL = 1
    EXPERIENCED = 2
    MANAGER = 3
    DIRECTOR = 4
    EXECUTIVE = 5


class JobView(enum.IntEnum):
    """
    An enum that specifies the job attributes that are returned in the
    ``MatchingJob.job`` or ``ListJobsResponse.jobs`` fields.

    Attributes:
      JOB_VIEW_UNSPECIFIED (int): Default value.
      JOB_VIEW_ID_ONLY (int): A ID only view of job, with following attributes: ``Job.name``,
      ``Job.requisition_id``, ``Job.language_code``.
      JOB_VIEW_MINIMAL (int): A minimal view of the job, with the following attributes: ``Job.name``,
      ``Job.requisition_id``, ``Job.title``, ``Job.company``,
      ``Job.DerivedInfo.locations``, ``Job.language_code``.
      JOB_VIEW_SMALL (int): A small view of the job, with the following attributes in the search
      results: ``Job.name``, ``Job.requisition_id``, ``Job.title``,
      ``Job.company``, ``Job.DerivedInfo.locations``, ``Job.visibility``,
      ``Job.language_code``, ``Job.description``.
      JOB_VIEW_FULL (int): All available attributes are included in the search results.
    """

    JOB_VIEW_UNSPECIFIED = 0
    JOB_VIEW_ID_ONLY = 1
    JOB_VIEW_MINIMAL = 2
    JOB_VIEW_SMALL = 3
    JOB_VIEW_FULL = 4


class Outcome(enum.IntEnum):
    """
    The overall outcome /decision / result indicator.

    Attributes:
      OUTCOME_UNSPECIFIED (int): Default value.
      POSITIVE (int): A positive outcome / passing indicator (for example, candidate was
      recommended for hiring or to be moved forward in the hiring process,
      candidate passed a test).
      NEUTRAL (int): A neutral outcome / no clear indicator (for example, no strong
      reccommendation either to move forward / not move forward, neutral score).
      NEGATIVE (int): A negative outcome / failing indicator (for example, candidate was
      recommended to NOT move forward in the hiring process, failed a test).
      OUTCOME_NOT_AVAILABLE (int): The assessment outcome is not available or otherwise unknown (for example,
      candidate did not complete assessment).
    """

    OUTCOME_UNSPECIFIED = 0
    POSITIVE = 1
    NEUTRAL = 2
    NEGATIVE = 3
    OUTCOME_NOT_AVAILABLE = 4


class PostingRegion(enum.IntEnum):
    """
    An enum that represents the job posting region. In most cases, job postings
    don't need to specify a region. If a region is given, jobs are
    eligible for searches in the specified region.

    Attributes:
      POSTING_REGION_UNSPECIFIED (int): If the region is unspecified, the job is only returned if it matches the
      ``LocationFilter``.
      ADMINISTRATIVE_AREA (int): In addition to exact location matching, job posting is returned when the
      ``LocationFilter`` in the search query is in the same administrative
      area as the returned job posting. For example, if a
      ``ADMINISTRATIVE_AREA`` job is posted in "CA, USA", it's returned if
      ``LocationFilter`` has "Mountain View".

      Administrative area refers to top-level administrative subdivision of
      this country. For example, US state, IT region, UK constituent nation
      and JP prefecture.
      NATION (int): In addition to exact location matching, job is returned when
      ``LocationFilter`` in search query is in the same country as this job.
      For example, if a ``NATION_WIDE`` job is posted in "USA", it's returned
      if ``LocationFilter`` has 'Mountain View'.
      TELECOMMUTE (int): Job allows employees to work remotely (telecommute).
      If locations are provided with this value, the job is
      considered as having a location, but telecommuting is allowed.
    """

    POSTING_REGION_UNSPECIFIED = 0
    ADMINISTRATIVE_AREA = 1
    NATION = 2
    TELECOMMUTE = 3


class SkillProficiencyLevel(enum.IntEnum):
    """
    Enum that represents the skill proficiency level.

    Attributes:
      SKILL_PROFICIENCY_LEVEL_UNSPECIFIED (int): Default value.
      UNSKILLED (int): Lacks any proficiency in this skill.
      FUNDAMENTAL_AWARENESS (int): Have a common knowledge or an understanding of basic techniques and
      concepts.
      NOVICE (int): Have the level of experience gained in a classroom and/or experimental
      scenarios or as a trainee on-the-job.
      INTERMEDIATE (int): Be able to successfully complete tasks in this skill as requested. Help
      from an expert may be required from time to time, but can usually perform
      skill independently.
      ADVANCED (int): Can perform the actions associated with this skill without assistance.
      EXPERT (int): Known as an expert in this area.
    """

    SKILL_PROFICIENCY_LEVEL_UNSPECIFIED = 0
    UNSKILLED = 6
    FUNDAMENTAL_AWARENESS = 1
    NOVICE = 2
    INTERMEDIATE = 3
    ADVANCED = 4
    EXPERT = 5


class Visibility(enum.IntEnum):
    """
    Deprecated. All resources are only visible to the owner.

    An enum that represents who has view access to the resource.

    Attributes:
      VISIBILITY_UNSPECIFIED (int): Default value.
      ACCOUNT_ONLY (int): The resource is only visible to the GCP account who owns it.
      SHARED_WITH_GOOGLE (int): The resource is visible to the owner and may be visible to other
      applications and processes at Google.
      SHARED_WITH_PUBLIC (int): The resource is visible to the owner and may be visible to all other API
      clients.
    """

    VISIBILITY_UNSPECIFIED = 0
    ACCOUNT_ONLY = 1
    SHARED_WITH_GOOGLE = 2
    SHARED_WITH_PUBLIC = 3


class Application(object):
    class ApplicationStage(enum.IntEnum):
        """
        The stage of the application.

        Attributes:
          APPLICATION_STAGE_UNSPECIFIED (int): Default value.
          NEW (int): Candidate has applied or a recruiter put candidate into consideration but
          candidate is not yet screened / no decision has been made to move or not
          move the candidate to the next stage.
          SCREEN (int): A recruiter decided to screen the candidate for this role.
          HIRING_MANAGER_REVIEW (int): Candidate is being / was sent to the customer / hiring manager for
          detailed review.
          INTERVIEW (int): Candidate was approved by the client / hiring manager and is being / was
          interviewed for the role.
          OFFER_EXTENDED (int): Candidate will be / has been given an offer of employment.
          OFFER_ACCEPTED (int): Candidate has accepted their offer of employment.
          STARTED (int): Candidate has begun (or completed) their employment or assignment with
          the employer.
        """

        APPLICATION_STAGE_UNSPECIFIED = 0
        NEW = 1
        SCREEN = 2
        HIRING_MANAGER_REVIEW = 3
        INTERVIEW = 4
        OFFER_EXTENDED = 5
        OFFER_ACCEPTED = 6
        STARTED = 7

    class ApplicationState(enum.IntEnum):
        """
        Enum that represents the application status.

        Attributes:
          APPLICATION_STATE_UNSPECIFIED (int): Default value.
          IN_PROGRESS (int): The current stage is in progress or pending, for example, interviews in
          progress.
          CANDIDATE_WITHDREW (int): The current stage was terminated by a candidate decision.
          EMPLOYER_WITHDREW (int): The current stage was terminated by an employer or agency decision.
          COMPLETED (int): The current stage is successfully completed, but the next stage (if
          applicable) has not begun.
          CLOSED (int): The current stage was closed without an exception, or terminated for
          reasons unrealated to the candidate.
        """

        APPLICATION_STATE_UNSPECIFIED = 0
        IN_PROGRESS = 1
        CANDIDATE_WITHDREW = 2
        EMPLOYER_WITHDREW = 3
        COMPLETED = 4
        CLOSED = 5


class BatchOperationMetadata(object):
    class State(enum.IntEnum):
        """
        Attributes:
          STATE_UNSPECIFIED (int): Default value.
          INITIALIZING (int): The batch operation is being prepared for processing.
          PROCESSING (int): The batch operation is actively being processed.
          SUCCEEDED (int): The batch operation is processed, and at least one item has been
          successfully processed.
          FAILED (int): The batch operation is done and no item has been successfully processed.
          CANCELLING (int): The batch operation is in the process of cancelling after
          ``google.longrunning.Operations.CancelOperation`` is called.
          CANCELLED (int): The batch operation is done after
          ``google.longrunning.Operations.CancelOperation`` is called. Any items
          processed before cancelling are returned in the response.
        """

        STATE_UNSPECIFIED = 0
        INITIALIZING = 1
        PROCESSING = 2
        SUCCEEDED = 3
        FAILED = 4
        CANCELLING = 5
        CANCELLED = 6


class CommuteFilter(object):
    class RoadTraffic(enum.IntEnum):
        """
        The traffic density to use when calculating commute time.

        Attributes:
          ROAD_TRAFFIC_UNSPECIFIED (int): Road traffic situation isn't specified.
          TRAFFIC_FREE (int): Optimal commute time without considering any traffic impact.
          BUSY_HOUR (int): Commute time calculation takes in account the peak traffic impact.
        """

        ROAD_TRAFFIC_UNSPECIFIED = 0
        TRAFFIC_FREE = 1
        BUSY_HOUR = 2


class CompensationFilter(object):
    class FilterType(enum.IntEnum):
        """
        Specify the type of filtering.

        Attributes:
          FILTER_TYPE_UNSPECIFIED (int): Filter type unspecified. Position holder, INVALID, should never be used.
          UNIT_ONLY (int): Filter by ``base compensation entry's`` unit. A job is a match if and
          only if the job contains a base CompensationEntry and the base
          CompensationEntry's unit matches provided ``units``. Populate one or
          more ``units``.

          See ``CompensationInfo.CompensationEntry`` for definition of base
          compensation entry.
          UNIT_AND_AMOUNT (int): Filter by ``base compensation entry's`` unit and amount / range. A job
          is a match if and only if the job contains a base CompensationEntry, and
          the base entry's unit matches provided ``CompensationUnit`` and amount
          or range overlaps with provided ``CompensationRange``.

          See ``CompensationInfo.CompensationEntry`` for definition of base
          compensation entry.

          Set exactly one ``units`` and populate ``range``.
          ANNUALIZED_BASE_AMOUNT (int): Filter by annualized base compensation amount and
          ``base compensation entry's`` unit. Populate ``range`` and zero or more
          ``units``.
          ANNUALIZED_TOTAL_AMOUNT (int): Filter by annualized total compensation amount and
          ``base compensation entry's`` unit . Populate ``range`` and zero or more
          ``units``.
        """

        FILTER_TYPE_UNSPECIFIED = 0
        UNIT_ONLY = 1
        UNIT_AND_AMOUNT = 2
        ANNUALIZED_BASE_AMOUNT = 3
        ANNUALIZED_TOTAL_AMOUNT = 4


class CompensationInfo(object):
    class CompensationType(enum.IntEnum):
        """
        The type of compensation.

        For compensation amounts specified in non-monetary amounts, describe the
        compensation scheme in the ``CompensationEntry.description``.

        For example, tipping format is described in
        ``CompensationEntry.description`` (for example, "expect 15-20% tips
        based on customer bill.") and an estimate of the tips provided in
        ``CompensationEntry.amount`` or ``CompensationEntry.range`` ($10 per
        hour).

        For example, equity is described in ``CompensationEntry.description``
        (for example, "1% - 2% equity vesting over 4 years, 1 year cliff") and
        value estimated in ``CompensationEntry.amount`` or
        ``CompensationEntry.range``. If no value estimate is possible, units are
        ``CompensationUnit.COMPENSATION_UNIT_UNSPECIFIED`` and then further
        clarified in ``CompensationEntry.description`` field.

        Attributes:
          COMPENSATION_TYPE_UNSPECIFIED (int): Default value.
          BASE (int): Base compensation: Refers to the fixed amount of money paid to an
          employee by an employer in return for work performed. Base compensation
          does not include benefits, bonuses or any other potential compensation
          from an employer.
          BONUS (int): Bonus.
          SIGNING_BONUS (int): Signing bonus.
          EQUITY (int): Equity.
          PROFIT_SHARING (int): Profit sharing.
          COMMISSIONS (int): Commission.
          TIPS (int): Tips.
          OTHER_COMPENSATION_TYPE (int): Other compensation type.
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

    class CompensationUnit(enum.IntEnum):
        """
        Pay frequency.

        Attributes:
          COMPENSATION_UNIT_UNSPECIFIED (int): Default value.
          HOURLY (int): Hourly.
          DAILY (int): Daily.
          WEEKLY (int): Weekly
          MONTHLY (int): Monthly.
          YEARLY (int): Yearly.
          ONE_TIME (int): One time.
          OTHER_COMPENSATION_UNIT (int): Other compensation units.
        """

        COMPENSATION_UNIT_UNSPECIFIED = 0
        HOURLY = 1
        DAILY = 2
        WEEKLY = 3
        MONTHLY = 4
        YEARLY = 5
        ONE_TIME = 6
        OTHER_COMPENSATION_UNIT = 7


class CompleteQueryRequest(object):
    class CompletionScope(enum.IntEnum):
        """
        Enum to specify the scope of completion.

        Attributes:
          COMPLETION_SCOPE_UNSPECIFIED (int): Default value.
          TENANT (int): Suggestions are based only on the data provided by the client.
          PUBLIC (int): Suggestions are based on all jobs data in the system that's visible to
          the client
        """

        COMPLETION_SCOPE_UNSPECIFIED = 0
        TENANT = 1
        PUBLIC = 2

    class CompletionType(enum.IntEnum):
        """
        Enum to specify auto-completion topics.

        Attributes:
          COMPLETION_TYPE_UNSPECIFIED (int): Default value.
          JOB_TITLE (int): Only suggest job titles.
          COMPANY_NAME (int): Only suggest company names.
          COMBINED (int): Suggest both job titles and company names.
        """

        COMPLETION_TYPE_UNSPECIFIED = 0
        JOB_TITLE = 1
        COMPANY_NAME = 2
        COMBINED = 3


class DeviceInfo(object):
    class DeviceType(enum.IntEnum):
        """
        An enumeration describing an API access portal and exposure mechanism.

        Attributes:
          DEVICE_TYPE_UNSPECIFIED (int): The device type isn't specified.
          WEB (int): A desktop web browser, such as, Chrome, Firefox, Safari, or Internet
          Explorer)
          MOBILE_WEB (int): A mobile device web browser, such as a phone or tablet with a Chrome
          browser.
          ANDROID (int): An Android device native application.
          IOS (int): An iOS device native application.
          BOT (int): A bot, as opposed to a device operated by human beings, such as a web
          crawler.
          OTHER (int): Other devices types.
        """

        DEVICE_TYPE_UNSPECIFIED = 0
        WEB = 1
        MOBILE_WEB = 2
        ANDROID = 3
        IOS = 4
        BOT = 5
        OTHER = 6


class EmployerFilter(object):
    class EmployerFilterMode(enum.IntEnum):
        """
        Enum indicating which set of ``Profile.employment_records`` to search
        against.

        Attributes:
          EMPLOYER_FILTER_MODE_UNSPECIFIED (int): Default value.
          ALL_EMPLOYMENT_RECORDS (int): Apply to all employers in ``Profile.employment_records``.
          CURRENT_EMPLOYMENT_RECORDS_ONLY (int): Apply only to current employer in ``Profile.employment_records``.
          PAST_EMPLOYMENT_RECORDS_ONLY (int): Apply only to past (not current) employers in
          ``Profile.employment_records``.
        """

        EMPLOYER_FILTER_MODE_UNSPECIFIED = 0
        ALL_EMPLOYMENT_RECORDS = 1
        CURRENT_EMPLOYMENT_RECORDS_ONLY = 2
        PAST_EMPLOYMENT_RECORDS_ONLY = 3


class JobEvent(object):
    class JobEventType(enum.IntEnum):
        """
        An enumeration of an event attributed to the behavior of the end user,
        such as a job seeker.

        Attributes:
          JOB_EVENT_TYPE_UNSPECIFIED (int): The event is unspecified by other provided values.
          IMPRESSION (int): The job seeker or other entity interacting with the service has
          had a job rendered in their view, such as in a list of search results in
          a compressed or clipped format. This event is typically associated with
          the viewing of a jobs list on a single page by a job seeker.
          VIEW (int): The job seeker, or other entity interacting with the service, has viewed
          the details of a job, including the full description. This event doesn't
          apply to the viewing a snippet of a job appearing as a part of the job
          search results. Viewing a snippet is associated with an ``impression``).
          VIEW_REDIRECT (int): The job seeker or other entity interacting with the service
          performed an action to view a job and was redirected to a different
          website for job.
          APPLICATION_START (int): The job seeker or other entity interacting with the service
          began the process or demonstrated the intention of applying for a job.
          APPLICATION_FINISH (int): The job seeker or other entity interacting with the service
          submitted an application for a job.
          APPLICATION_QUICK_SUBMISSION (int): The job seeker or other entity interacting with the service submitted an
          application for a job with a single click without entering information.
          If a job seeker performs this action, send only this event to the
          service. Do not also send ``JobEventType.APPLICATION_START`` or
          ``JobEventType.APPLICATION_FINISH`` events.
          APPLICATION_REDIRECT (int): The job seeker or other entity interacting with the service
          performed an action to apply to a job and was redirected to a different
          website to complete the application.
          APPLICATION_START_FROM_SEARCH (int): The job seeker or other entity interacting with the service began the
          process or demonstrated the intention of applying for a job from the
          search results page without viewing the details of the job posting.
          If sending this event, JobEventType.VIEW event shouldn't be sent.
          APPLICATION_REDIRECT_FROM_SEARCH (int): The job seeker, or other entity interacting with the service, performs
          an action with a single click from the search results page to apply to a
          job (without viewing the details of the job posting), and is redirected
          to a different website to complete the application. If a candidate
          performs this action, send only this event to the service. Do not also
          send ``JobEventType.APPLICATION_START``,
          ``JobEventType.APPLICATION_FINISH`` or ``JobEventType.VIEW`` events.
          APPLICATION_COMPANY_SUBMIT (int): This event should be used when a company submits an application
          on behalf of a job seeker. This event is intended for use by staffing
          agencies attempting to place candidates.
          BOOKMARK (int): The job seeker or other entity interacting with the service demonstrated
          an interest in a job by bookmarking or saving it.
          NOTIFICATION (int): The job seeker or other entity interacting with the service was
          sent a notification, such as an email alert or device notification,
          containing one or more jobs listings generated by the service.
          HIRED (int): The job seeker or other entity interacting with the service was
          employed by the hiring entity (employer). Send this event
          only if the job seeker was hired through an application that was
          initiated by a search conducted through the Cloud Talent Solution
          service.
          SENT_CV (int): A recruiter or staffing agency submitted an application on behalf of the
          candidate after interacting with the service to identify a suitable job
          posting.
          INTERVIEW_GRANTED (int): The entity interacting with the service (for example, the job seeker),
          was granted an initial interview by the hiring entity (employer). This
          event should only be sent if the job seeker was granted an interview as
          part of an application that was initiated by a search conducted through /
          recommendation provided by the Cloud Talent Solution service.
        """

        JOB_EVENT_TYPE_UNSPECIFIED = 0
        IMPRESSION = 1
        VIEW = 2
        VIEW_REDIRECT = 3
        APPLICATION_START = 4
        APPLICATION_FINISH = 5
        APPLICATION_QUICK_SUBMISSION = 6
        APPLICATION_REDIRECT = 7
        APPLICATION_START_FROM_SEARCH = 8
        APPLICATION_REDIRECT_FROM_SEARCH = 9
        APPLICATION_COMPANY_SUBMIT = 10
        BOOKMARK = 11
        NOTIFICATION = 12
        HIRED = 13
        SENT_CV = 14
        INTERVIEW_GRANTED = 15


class Location(object):
    class LocationType(enum.IntEnum):
        """
        An enum which represents the type of a location.

        Attributes:
          LOCATION_TYPE_UNSPECIFIED (int): Default value if the type isn't specified.
          COUNTRY (int): A country level location.
          ADMINISTRATIVE_AREA (int): A state or equivalent level location.
          SUB_ADMINISTRATIVE_AREA (int): A county or equivalent level location.
          LOCALITY (int): A city or equivalent level location.
          POSTAL_CODE (int): A postal code level location.
          SUB_LOCALITY (int): A sublocality is a subdivision of a locality, for example a city borough,
          ward, or arrondissement. Sublocalities are usually recognized by a local
          political authority. For example, Manhattan and Brooklyn are recognized
          as boroughs by the City of New York, and are therefore modeled as
          sublocalities.
          SUB_LOCALITY_1 (int): A district or equivalent level location.
          SUB_LOCALITY_2 (int): A smaller district or equivalent level display.
          NEIGHBORHOOD (int): A neighborhood level location.
          STREET_ADDRESS (int): A street address level location.
        """

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


class LocationFilter(object):
    class TelecommutePreference(enum.IntEnum):
        """
        Specify whether to include telecommute jobs.

        Attributes:
          TELECOMMUTE_PREFERENCE_UNSPECIFIED (int): Default value if the telecommute preference isn't specified.
          TELECOMMUTE_EXCLUDED (int): Exclude telecommute jobs.
          TELECOMMUTE_ALLOWED (int): Allow telecommute jobs.
        """

        TELECOMMUTE_PREFERENCE_UNSPECIFIED = 0
        TELECOMMUTE_EXCLUDED = 1
        TELECOMMUTE_ALLOWED = 2


class Phone(object):
    class PhoneType(enum.IntEnum):
        """
        Enum that represents the type of the telephone.

        Attributes:
          PHONE_TYPE_UNSPECIFIED (int): Default value.
          LANDLINE (int): A landline.
          MOBILE (int): A mobile.
          FAX (int): A fax.
          PAGER (int): A pager.
          TTY_OR_TDD (int): A TTY (test telephone) or TDD (telecommunication device for the deaf).
          VOICEMAIL (int): A voicemail.
          VIRTUAL (int): A virtual telephone number is a number that can be routed to another
          number and managed by the user via Web, SMS, IVR, and so on. It is
          associated with a particular person, and may be routed to either a
          MOBILE or LANDLINE number. The ``phone usage`` should be set to PERSONAL
          for these phone types. Some more information can be found here:
          http://en.wikipedia.org/wiki/Personal\_Numbers
          VOIP (int): Voice over IP numbers. This includes TSoIP (Telephony Service over IP).
          MOBILE_OR_LANDLINE (int): In some regions (e.g. the USA), it is impossible to distinguish between
          fixed-line and mobile numbers by looking at the phone number itself.
        """

        PHONE_TYPE_UNSPECIFIED = 0
        LANDLINE = 1
        MOBILE = 2
        FAX = 3
        PAGER = 4
        TTY_OR_TDD = 5
        VOICEMAIL = 6
        VIRTUAL = 7
        VOIP = 8
        MOBILE_OR_LANDLINE = 9


class ProfileEvent(object):
    class ProfileEventType(enum.IntEnum):
        """
        The enum represents types of client events for a candidate profile.

        Attributes:
          PROFILE_EVENT_TYPE_UNSPECIFIED (int): Default value.
          IMPRESSION (int): Send this event when a ``ProfileEvent.profiles`` was sent as a part of a
          result set for a CTS API call and was rendered in the end user's UI
          (that is, the ``ProfileEvent.recruiter``).
          VIEW (int): The VIEW event records the action of a candidate's profile being viewed
          by an end user. This is critical to tracking product metrics and should
          be sent for every profile VIEW that happens in your system, whether the
          event is associated with an API call (for example, a recruiter making a
          request for a result set and clicking on a profile) or not (a recruiter
          using the system to view profile details without making a request).

          For a VIEW events associated with API calls, the
          ``ClientEvent.request_id`` should be populated. If the VIEW is not
          associated with an API call, ``request_id`` should not be populated.

          This event requires a valid recruiter and one valid ID in profiles.
          BOOKMARK (int): The profile is bookmarked.
        """

        PROFILE_EVENT_TYPE_UNSPECIFIED = 0
        IMPRESSION = 1
        VIEW = 2
        BOOKMARK = 3


class Resume(object):
    class ResumeType(enum.IntEnum):
        """
        The format of a structured resume.

        Attributes:
          RESUME_TYPE_UNSPECIFIED (int): Default value.
          HRXML (int): The profile contents in HR-XML format.
          See http://schemas.liquid-technologies.com/hr-xml/2007-04-15/ for more
          information about Human Resources XML.
          OTHER_RESUME_TYPE (int): Resume type not specified.
        """

        RESUME_TYPE_UNSPECIFIED = 0
        HRXML = 1
        OTHER_RESUME_TYPE = 2


class SearchJobsRequest(object):
    class DiversificationLevel(enum.IntEnum):
        """
        Controls whether highly similar jobs are returned next to each other in
        the search results. Jobs are identified as highly similar based on
        their titles, job categories, and locations. Highly similar results are
        clustered so that only one representative job of the cluster is
        displayed to the job seeker higher up in the results, with the other jobs
        being displayed lower down in the results.

        Attributes:
          DIVERSIFICATION_LEVEL_UNSPECIFIED (int): The diversification level isn't specified.
          DISABLED (int): Disables diversification. Jobs that would normally be pushed to the last
          page would not have their positions altered. This may result in highly
          similar jobs appearing in sequence in the search results.
          SIMPLE (int): Default diversifying behavior. The result list is ordered so that
          highly similar results are pushed to the end of the last page of search
          results.
        """

        DIVERSIFICATION_LEVEL_UNSPECIFIED = 0
        DISABLED = 1
        SIMPLE = 2

    class SearchMode(enum.IntEnum):
        """
        A string-represented enumeration of the job search mode. The service
        operate differently for different modes of service.

        Attributes:
          SEARCH_MODE_UNSPECIFIED (int): The mode of the search method isn't specified.
          JOB_SEARCH (int): The job search matches against all jobs, and featured jobs
          (jobs with promotionValue > 0) are not specially handled.
          FEATURED_JOB_SEARCH (int): The job search matches only against featured jobs (jobs with a
          promotionValue > 0). This method doesn't return any jobs having a
          promotionValue <= 0. The search results order is determined by the
          promotionValue (jobs with a higher promotionValue are returned higher up
          in the search results), with relevance being used as a tiebreaker.
        """

        SEARCH_MODE_UNSPECIFIED = 0
        JOB_SEARCH = 1
        FEATURED_JOB_SEARCH = 2

    class CustomRankingInfo(object):
        class ImportanceLevel(enum.IntEnum):
            """
            The importance level for ``CustomRankingInfo.ranking_expression``.

            Attributes:
              IMPORTANCE_LEVEL_UNSPECIFIED (int): Default value if the importance level isn't specified.
              NONE (int): The given ranking expression is of None importance, existing relevance
              score (determined by API algorithm) dominates job's final ranking
              position.
              LOW (int): The given ranking expression is of Low importance in terms of job's
              final ranking position compared to existing relevance
              score (determined by API algorithm).
              MILD (int): The given ranking expression is of Mild importance in terms of job's
              final ranking position compared to existing relevance
              score (determined by API algorithm).
              MEDIUM (int): The given ranking expression is of Medium importance in terms of job's
              final ranking position compared to existing relevance
              score (determined by API algorithm).
              HIGH (int): The given ranking expression is of High importance in terms of job's
              final ranking position compared to existing relevance
              score (determined by API algorithm).
              EXTREME (int): The given ranking expression is of Extreme importance, and dominates
              job's final ranking position with existing relevance
              score (determined by API algorithm) ignored.
            """

            IMPORTANCE_LEVEL_UNSPECIFIED = 0
            NONE = 1
            LOW = 2
            MILD = 3
            MEDIUM = 4
            HIGH = 5
            EXTREME = 6


class Tenant(object):
    class DataUsageType(enum.IntEnum):
        """
        Enum that represents how user data owned by the tenant is used.

        Attributes:
          DATA_USAGE_TYPE_UNSPECIFIED (int): Default value.
          AGGREGATED (int): Data owned by this tenant is used to improve search/recommendation
          quality across tenants.
          ISOLATED (int): Data owned by this tenant is used to improve search/recommendation
          quality for this tenant only.
        """

        DATA_USAGE_TYPE_UNSPECIFIED = 0
        AGGREGATED = 1
        ISOLATED = 2


class TimeFilter(object):
    class TimeField(enum.IntEnum):
        """
        Time fields can be used in TimeFilter.

        Attributes:
          TIME_FIELD_UNSPECIFIED (int): Default value.
          CREATE_TIME (int): Earliest profile create time.
          UPDATE_TIME (int): Latest profile update time.
        """

        TIME_FIELD_UNSPECIFIED = 0
        CREATE_TIME = 1
        UPDATE_TIME = 2
