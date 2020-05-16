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


from google.cloud.osconfig_v1.types import patch_jobs
from google.protobuf import duration_pb2 as gp_duration  # type: ignore
from google.protobuf import timestamp_pb2 as timestamp  # type: ignore
from google.type import datetime_pb2 as datetime  # type: ignore
from google.type import dayofweek_pb2 as dayofweek  # type: ignore
from google.type import timeofday_pb2 as timeofday  # type: ignore


__protobuf__ = proto.module(
    package="google.cloud.osconfig.v1",
    manifest={
        "PatchDeployment",
        "OneTimeSchedule",
        "RecurringSchedule",
        "WeeklySchedule",
        "MonthlySchedule",
        "WeekDayOfMonth",
        "CreatePatchDeploymentRequest",
        "GetPatchDeploymentRequest",
        "ListPatchDeploymentsRequest",
        "ListPatchDeploymentsResponse",
        "DeletePatchDeploymentRequest",
    },
)


class PatchDeployment(proto.Message):
    r"""Patch deployments are configurations that individual patch jobs use
    to complete a patch. These configurations include instance filter,
    package repository settings, and a schedule. For more information
    about creating and managing patch deployments, see `Scheduling patch
    jobs <https://cloud.google.com/compute/docs/os-patch-management/schedule-patch-jobs>`__.

    Attributes:
        name (str):
            Unique name for the patch deployment resource in a project.
            The patch deployment name is in the form:
            ``projects/{project_id}/patchDeployments/{patch_deployment_id}``.
            This field is ignored when you create a new patch
            deployment.
        description (str):
            Optional. Description of the patch
            deployment. Length of the description is limited
            to 1024 characters.
        instance_filter (~.patch_jobs.PatchInstanceFilter):
            Required. VM instances to patch.
        patch_config (~.patch_jobs.PatchConfig):
            Optional. Patch configuration that is
            applied.
        duration (~.gp_duration.Duration):
            Optional. Duration of the patch. After the
            duration ends, the patch times out.
        one_time_schedule (~.gco_patch_deployments.OneTimeSchedule):
            Required. Schedule a one-time execution.
        recurring_schedule (~.gco_patch_deployments.RecurringSchedule):
            Required. Schedule recurring executions.
        create_time (~.timestamp.Timestamp):
            Output only. Time the patch deployment was created.
            Timestamp is in
            `RFC3339 <https://www.ietf.org/rfc/rfc3339.txt>`__ text
            format.
        update_time (~.timestamp.Timestamp):
            Output only. Time the patch deployment was last updated.
            Timestamp is in
            `RFC3339 <"https://www.ietf.org/rfc/rfc3339.txt>`__ text
            format.
        last_execute_time (~.timestamp.Timestamp):
            Output only. The last time a patch job was started by this
            deployment. Timestamp is in
            `RFC3339 <https://www.ietf.org/rfc/rfc3339.txt>`__ text
            format.
    """

    name = proto.Field(proto.STRING, number=1)
    description = proto.Field(proto.STRING, number=2)
    instance_filter = proto.Field(
        proto.MESSAGE, number=3, message=patch_jobs.PatchInstanceFilter
    )
    patch_config = proto.Field(proto.MESSAGE, number=4, message=patch_jobs.PatchConfig)
    duration = proto.Field(proto.MESSAGE, number=5, message=gp_duration.Duration)
    one_time_schedule = proto.Field(proto.MESSAGE, number=6, message="OneTimeSchedule")
    recurring_schedule = proto.Field(
        proto.MESSAGE, number=7, message="RecurringSchedule"
    )
    create_time = proto.Field(proto.MESSAGE, number=8, message=timestamp.Timestamp)
    update_time = proto.Field(proto.MESSAGE, number=9, message=timestamp.Timestamp)
    last_execute_time = proto.Field(
        proto.MESSAGE, number=10, message=timestamp.Timestamp
    )


class OneTimeSchedule(proto.Message):
    r"""Sets the time for a one time patch deployment. Timestamp is in
    `RFC3339 <https://www.ietf.org/rfc/rfc3339.txt>`__ text format.

    Attributes:
        execute_time (~.timestamp.Timestamp):
            Required. The desired patch job execution
            time.
    """

    execute_time = proto.Field(proto.MESSAGE, number=1, message=timestamp.Timestamp)


class RecurringSchedule(proto.Message):
    r"""Sets the time for recurring patch deployments.

    Attributes:
        time_zone (~.datetime.TimeZone):
            Required. Defines the time zone that ``time_of_day`` is
            relative to. The rules for daylight saving time are
            determined by the chosen time zone.
        start_time (~.timestamp.Timestamp):
            Optional. The time that the recurring schedule becomes
            effective. Defaults to ``create_time`` of the patch
            deployment.
        end_time (~.timestamp.Timestamp):
            Optional. The end time at which a recurring
            patch deployment schedule is no longer active.
        time_of_day (~.timeofday.TimeOfDay):
            Required. Time of the day to run a recurring
            deployment.
        frequency (~.gco_patch_deployments.RecurringSchedule.Frequency):
            Required. The frequency unit of this
            recurring schedule.
        weekly (~.gco_patch_deployments.WeeklySchedule):
            Required. Schedule with weekly executions.
        monthly (~.gco_patch_deployments.MonthlySchedule):
            Required. Schedule with monthly executions.
        last_execute_time (~.timestamp.Timestamp):
            Output only. The time the last patch job ran
            successfully.
        next_execute_time (~.timestamp.Timestamp):
            Output only. The time the next patch job is
            scheduled to run.
    """

    class Frequency(proto.Enum):
        r"""Specifies the frequency of the recurring patch deployments."""
        FREQUENCY_UNSPECIFIED = 0
        WEEKLY = 1
        MONTHLY = 2

    time_zone = proto.Field(proto.MESSAGE, number=1, message=datetime.TimeZone)
    start_time = proto.Field(proto.MESSAGE, number=2, message=timestamp.Timestamp)
    end_time = proto.Field(proto.MESSAGE, number=3, message=timestamp.Timestamp)
    time_of_day = proto.Field(proto.MESSAGE, number=4, message=timeofday.TimeOfDay)
    frequency = proto.Field(proto.ENUM, number=5, enum=Frequency)
    weekly = proto.Field(proto.MESSAGE, number=6, message="WeeklySchedule")
    monthly = proto.Field(proto.MESSAGE, number=7, message="MonthlySchedule")
    last_execute_time = proto.Field(
        proto.MESSAGE, number=9, message=timestamp.Timestamp
    )
    next_execute_time = proto.Field(
        proto.MESSAGE, number=10, message=timestamp.Timestamp
    )


class WeeklySchedule(proto.Message):
    r"""Represents a weekly schedule.

    Attributes:
        day_of_week (~.dayofweek.DayOfWeek):
            Required. Day of the week.
    """

    day_of_week = proto.Field(proto.ENUM, number=1, enum=dayofweek.DayOfWeek)


class MonthlySchedule(proto.Message):
    r"""Represents a monthly schedule. An example of a valid monthly
    schedule is "on the third Tuesday of the month" or "on the 15th
    of the month".

    Attributes:
        week_day_of_month (~.gco_patch_deployments.WeekDayOfMonth):
            Required. Week day in a month.
        month_day (int):
            Required. One day of the month. 1-31
            indicates the 1st to the 31st day. -1 indicates
            the last day of the month. Months without the
            target day will be skipped. For example, a
            schedule to run "every month on the 31st" will
            not run in February, April, June, etc.
    """

    week_day_of_month = proto.Field(proto.MESSAGE, number=1, message="WeekDayOfMonth")
    month_day = proto.Field(proto.INT32, number=2)


class WeekDayOfMonth(proto.Message):
    r"""Represents one week day in a month. An example is "the 4th
    Sunday".

    Attributes:
        week_ordinal (int):
            Required. Week number in a month. 1-4
            indicates the 1st to 4th week of the month. -1
            indicates the last week of the month.
        day_of_week (~.dayofweek.DayOfWeek):
            Required. A day of the week.
    """

    week_ordinal = proto.Field(proto.INT32, number=1)
    day_of_week = proto.Field(proto.ENUM, number=2, enum=dayofweek.DayOfWeek)


class CreatePatchDeploymentRequest(proto.Message):
    r"""A request message for creating a patch deployment.

    Attributes:
        parent (str):
            Required. The project to apply this patch deployment to in
            the form ``projects/*``.
        patch_deployment_id (str):
            Required. A name for the patch deployment in the project.
            When creating a name the following rules apply:

            -  Must contain only lowercase letters, numbers, and
               hyphens.
            -  Must start with a letter.
            -  Must be between 1-63 characters.
            -  Must end with a number or a letter.
            -  Must be unique within the project.
        patch_deployment (~.gco_patch_deployments.PatchDeployment):
            Required. The patch deployment to create.
    """

    parent = proto.Field(proto.STRING, number=1)
    patch_deployment_id = proto.Field(proto.STRING, number=2)
    patch_deployment = proto.Field(proto.MESSAGE, number=3, message=PatchDeployment)


class GetPatchDeploymentRequest(proto.Message):
    r"""A request message for retrieving a patch deployment.

    Attributes:
        name (str):
            Required. The resource name of the patch deployment in the
            form ``projects/*/patchDeployments/*``.
    """

    name = proto.Field(proto.STRING, number=1)


class ListPatchDeploymentsRequest(proto.Message):
    r"""A request message for listing patch deployments.

    Attributes:
        parent (str):
            Required. The resource name of the parent in the form
            ``projects/*``.
        page_size (int):
            Optional. The maximum number of patch
            deployments to return. Default is 100.
        page_token (str):
            Optional. A pagination token returned from a
            previous call to ListPatchDeployments that
            indicates where this listing should continue
            from.
    """

    parent = proto.Field(proto.STRING, number=1)
    page_size = proto.Field(proto.INT32, number=2)
    page_token = proto.Field(proto.STRING, number=3)


class ListPatchDeploymentsResponse(proto.Message):
    r"""A response message for listing patch deployments.

    Attributes:
        patch_deployments (Sequence[~.gco_patch_deployments.PatchDeployment]):
            The list of patch deployments.
        next_page_token (str):
            A pagination token that can be used to get
            the next page of patch deployments.
    """

    @property
    def raw_page(self):
        return self

    patch_deployments = proto.RepeatedField(
        proto.MESSAGE, number=1, message=PatchDeployment
    )
    next_page_token = proto.Field(proto.STRING, number=2)


class DeletePatchDeploymentRequest(proto.Message):
    r"""A request message for deleting a patch deployment.

    Attributes:
        name (str):
            Required. The resource name of the patch deployment in the
            form ``projects/*/patchDeployments/*``.
    """

    name = proto.Field(proto.STRING, number=1)


__all__ = tuple(sorted(__protobuf__.manifest))
