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
from google.protobuf import timestamp_pb2  # type: ignore
from google.protobuf import wrappers_pb2  # type: ignore
from google.type import date_pb2  # type: ignore


__protobuf__ = proto.module(
    package="google.cloud.talent.v4beta1", manifest={"Application",},
)


class Application(proto.Message):
    r"""Resource that represents a job application record of a
    candidate.

    Attributes:
        name (str):
            Required during application update.

            Resource name assigned to an application by the API.

            The format is
            "projects/{project_id}/tenants/{tenant_id}/profiles/{profile_id}/applications/{application_id}".
            For example,
            "projects/foo/tenants/bar/profiles/baz/applications/qux".
        external_id (str):
            Required. Client side application identifier,
            used to uniquely identify the application.

            The maximum number of allowed characters is 255.
        profile (str):
            Output only. Resource name of the candidate of this
            application.

            The format is
            "projects/{project_id}/tenants/{tenant_id}/profiles/{profile_id}".
            For example, "projects/foo/tenants/bar/profiles/baz".
        job (str):
            Required. Resource name of the job which the candidate
            applied for.

            The format is
            "projects/{project_id}/tenants/{tenant_id}/jobs/{job_id}".
            For example, "projects/foo/tenants/bar/jobs/baz".
        company (str):
            Resource name of the company which the candidate applied
            for.

            The format is
            "projects/{project_id}/tenants/{tenant_id}/companies/{company_id}".
            For example, "projects/foo/tenants/bar/companies/baz".
        application_date (google.type.date_pb2.Date):
            The application date.
        stage (google.cloud.talent_v4beta1.types.Application.ApplicationStage):
            Required. What is the most recent stage of
            the application (that is, new, screen, send cv,
            hired, finished work)?  This field is
            intentionally not comprehensive of every
            possible status, but instead, represents
            statuses that would be used to indicate to the
            ML models good / bad matches.
        state (google.cloud.talent_v4beta1.types.Application.ApplicationState):
            The application state.
        interviews (Sequence[google.cloud.talent_v4beta1.types.Interview]):
            All interviews (screen, onsite, and so on)
            conducted as part of this application (includes
            details such as user conducting the interview,
            timestamp, feedback, and so on).
        referral (google.protobuf.wrappers_pb2.BoolValue):
            If the candidate is referred by a employee.
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Required. Reflects the time that the
            application was created.
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            The last update timestamp.
        outcome_notes (str):
            Free text reason behind the recruitement
            outcome (for example, reason for withdraw /
            reject, reason for an unsuccessful finish, and
            so on).
            Number of characters allowed is 100.
        outcome (google.cloud.talent_v4beta1.types.Outcome):
            Outcome positiveness shows how positive the
            outcome is.
        is_match (google.protobuf.wrappers_pb2.BoolValue):
            Output only. Indicates whether this job
            application is a match to application related
            filters. This value is only applicable in
            profile search response.
        job_title_snippet (str):
            Output only. Job title snippet shows how the
            job title is related to a search query. It's
            empty if the job title isn't related to the
            search query.
    """

    class ApplicationState(proto.Enum):
        r"""Enum that represents the application status."""
        APPLICATION_STATE_UNSPECIFIED = 0
        IN_PROGRESS = 1
        CANDIDATE_WITHDREW = 2
        EMPLOYER_WITHDREW = 3
        COMPLETED = 4
        CLOSED = 5

    class ApplicationStage(proto.Enum):
        r"""The stage of the application."""
        APPLICATION_STAGE_UNSPECIFIED = 0
        NEW = 1
        SCREEN = 2
        HIRING_MANAGER_REVIEW = 3
        INTERVIEW = 4
        OFFER_EXTENDED = 5
        OFFER_ACCEPTED = 6
        STARTED = 7

    name = proto.Field(proto.STRING, number=1,)
    external_id = proto.Field(proto.STRING, number=31,)
    profile = proto.Field(proto.STRING, number=2,)
    job = proto.Field(proto.STRING, number=4,)
    company = proto.Field(proto.STRING, number=5,)
    application_date = proto.Field(proto.MESSAGE, number=7, message=date_pb2.Date,)
    stage = proto.Field(proto.ENUM, number=11, enum=ApplicationStage,)
    state = proto.Field(proto.ENUM, number=13, enum=ApplicationState,)
    interviews = proto.RepeatedField(
        proto.MESSAGE, number=16, message=common.Interview,
    )
    referral = proto.Field(proto.MESSAGE, number=18, message=wrappers_pb2.BoolValue,)
    create_time = proto.Field(
        proto.MESSAGE, number=19, message=timestamp_pb2.Timestamp,
    )
    update_time = proto.Field(
        proto.MESSAGE, number=20, message=timestamp_pb2.Timestamp,
    )
    outcome_notes = proto.Field(proto.STRING, number=21,)
    outcome = proto.Field(proto.ENUM, number=22, enum=common.Outcome,)
    is_match = proto.Field(proto.MESSAGE, number=28, message=wrappers_pb2.BoolValue,)
    job_title_snippet = proto.Field(proto.STRING, number=29,)


__all__ = tuple(sorted(__protobuf__.manifest))
