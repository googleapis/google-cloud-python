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


from google.protobuf import duration_pb2 as gp_duration  # type: ignore
from google.protobuf import timestamp_pb2 as timestamp  # type: ignore


__protobuf__ = proto.module(
    package="google.cloud.osconfig.v1",
    manifest={
        "ExecutePatchJobRequest",
        "GetPatchJobRequest",
        "ListPatchJobInstanceDetailsRequest",
        "ListPatchJobInstanceDetailsResponse",
        "PatchJobInstanceDetails",
        "ListPatchJobsRequest",
        "ListPatchJobsResponse",
        "PatchJob",
        "PatchConfig",
        "Instance",
        "CancelPatchJobRequest",
        "AptSettings",
        "YumSettings",
        "GooSettings",
        "ZypperSettings",
        "WindowsUpdateSettings",
        "ExecStep",
        "ExecStepConfig",
        "GcsObject",
        "PatchInstanceFilter",
    },
)


class ExecutePatchJobRequest(proto.Message):
    r"""A request message to initiate patching across Compute Engine
    instances.

    Attributes:
        parent (str):
            Required. The project in which to run this patch in the form
            ``projects/*``
        description (str):
            Description of the patch job. Length of the
            description is limited to 1024 characters.
        instance_filter (~.gco_patch_jobs.PatchInstanceFilter):
            Required. Instances to patch, either
            explicitly or filtered by some criteria such as
            zone or labels.
        patch_config (~.gco_patch_jobs.PatchConfig):
            Patch configuration being applied. If
            omitted, instances are patched using the default
            configurations.
        duration (~.gp_duration.Duration):
            Duration of the patch job. After the duration
            ends, the patch job times out.
        dry_run (bool):
            If this patch is a dry-run only, instances
            are contacted but will do nothing.
        display_name (str):
            Display name for this patch job. This does
            not have to be unique.
    """

    parent = proto.Field(proto.STRING, number=1)
    description = proto.Field(proto.STRING, number=2)
    instance_filter = proto.Field(
        proto.MESSAGE, number=7, message="PatchInstanceFilter"
    )
    patch_config = proto.Field(proto.MESSAGE, number=4, message="PatchConfig")
    duration = proto.Field(proto.MESSAGE, number=5, message=gp_duration.Duration)
    dry_run = proto.Field(proto.BOOL, number=6)
    display_name = proto.Field(proto.STRING, number=8)


class GetPatchJobRequest(proto.Message):
    r"""Request to get an active or completed patch job.

    Attributes:
        name (str):
            Required. Name of the patch in the form
            ``projects/*/patchJobs/*``
    """

    name = proto.Field(proto.STRING, number=1)


class ListPatchJobInstanceDetailsRequest(proto.Message):
    r"""Request to list details for all instances that are part of a
    patch job.

    Attributes:
        parent (str):
            Required. The parent for the instances are in the form of
            ``projects/*/patchJobs/*``.
        page_size (int):
            The maximum number of instance details
            records to return.  Default is 100.
        page_token (str):
            A pagination token returned from a previous
            call that indicates where this listing should
            continue from.
        filter (str):
            A filter expression that filters results listed in the
            response. This field supports filtering results by instance
            zone, name, state, or ``failure_reason``.
    """

    parent = proto.Field(proto.STRING, number=1)
    page_size = proto.Field(proto.INT32, number=2)
    page_token = proto.Field(proto.STRING, number=3)
    filter = proto.Field(proto.STRING, number=4)


class ListPatchJobInstanceDetailsResponse(proto.Message):
    r"""A response message for listing the instances details for a
    patch job.

    Attributes:
        patch_job_instance_details (Sequence[~.gco_patch_jobs.PatchJobInstanceDetails]):
            A list of instance status.
        next_page_token (str):
            A pagination token that can be used to get
            the next page of results.
    """

    @property
    def raw_page(self):
        return self

    patch_job_instance_details = proto.RepeatedField(
        proto.MESSAGE, number=1, message="PatchJobInstanceDetails"
    )
    next_page_token = proto.Field(proto.STRING, number=2)


class PatchJobInstanceDetails(proto.Message):
    r"""Patch details for a VM instance. For more information about
    reviewing VM instance details, see `Listing all VM instance details
    for a specific patch
    job <https://cloud.google.com/compute/docs/os-patch-management/manage-patch-jobs#list-instance-details>`__.

    Attributes:
        name (str):
            The instance name in the form
            ``projects/*/zones/*/instances/*``
        instance_system_id (str):
            The unique identifier for the instance. This
            identifier is defined by the server.
        state (~.gco_patch_jobs.Instance.PatchState):
            Current state of instance patch.
        failure_reason (str):
            If the patch fails, this field provides the
            reason.
        attempt_count (int):
            The number of times the agent that the agent
            attempts to apply the patch.
    """

    name = proto.Field(proto.STRING, number=1)
    instance_system_id = proto.Field(proto.STRING, number=2)
    state = proto.Field(proto.ENUM, number=3, enum="Instance.PatchState")
    failure_reason = proto.Field(proto.STRING, number=4)
    attempt_count = proto.Field(proto.INT64, number=5)


class ListPatchJobsRequest(proto.Message):
    r"""A request message for listing patch jobs.

    Attributes:
        parent (str):
            Required. In the form of ``projects/*``
        page_size (int):
            The maximum number of instance status to
            return.
        page_token (str):
            A pagination token returned from a previous
            call that indicates where this listing should
            continue from.
        filter (str):
            If provided, this field specifies the criteria that must be
            met by patch jobs to be included in the response. Currently,
            filtering is only available on the patch_deployment field.
    """

    parent = proto.Field(proto.STRING, number=1)
    page_size = proto.Field(proto.INT32, number=2)
    page_token = proto.Field(proto.STRING, number=3)
    filter = proto.Field(proto.STRING, number=4)


class ListPatchJobsResponse(proto.Message):
    r"""A response message for listing patch jobs.

    Attributes:
        patch_jobs (Sequence[~.gco_patch_jobs.PatchJob]):
            The list of patch jobs.
        next_page_token (str):
            A pagination token that can be used to get
            the next page of results.
    """

    @property
    def raw_page(self):
        return self

    patch_jobs = proto.RepeatedField(proto.MESSAGE, number=1, message="PatchJob")
    next_page_token = proto.Field(proto.STRING, number=2)


class PatchJob(proto.Message):
    r"""A high level representation of a patch job that is either in
    progress or has completed.

    Instances details are not included in the job. To paginate through
    instance details, use ListPatchJobInstanceDetails.

    For more information about patch jobs, see `Creating patch
    jobs <https://cloud.google.com/compute/docs/os-patch-management/create-patch-job>`__.

    Attributes:
        name (str):
            Unique identifier for this patch job in the form
            ``projects/*/patchJobs/*``
        display_name (str):
            Display name for this patch job. This is not
            a unique identifier.
        description (str):
            Description of the patch job. Length of the
            description is limited to 1024 characters.
        create_time (~.timestamp.Timestamp):
            Time this patch job was created.
        update_time (~.timestamp.Timestamp):
            Last time this patch job was updated.
        state (~.gco_patch_jobs.PatchJob.State):
            The current state of the PatchJob .
        instance_filter (~.gco_patch_jobs.PatchInstanceFilter):
            Instances to patch.
        patch_config (~.gco_patch_jobs.PatchConfig):
            Patch configuration being applied.
        duration (~.gp_duration.Duration):
            Duration of the patch job. After the duration
            ends, the patch job times out.
        instance_details_summary (~.gco_patch_jobs.PatchJob.InstanceDetailsSummary):
            Summary of instance details.
        dry_run (bool):
            If this patch job is a dry run, the agent
            reports that it has finished without running any
            updates on the VM instance.
        error_message (str):
            If this patch job failed, this message
            provides information about the failure.
        percent_complete (float):
            Reflects the overall progress of the patch
            job in the range of 0.0 being no progress to
            100.0 being complete.
        patch_deployment (str):
            Output only. Name of the patch deployment
            that created this patch job.
    """

    class State(proto.Enum):
        r"""Enumeration of the various states a patch job passes through
        as it executes.
        """
        STATE_UNSPECIFIED = 0
        STARTED = 1
        INSTANCE_LOOKUP = 2
        PATCHING = 3
        SUCCEEDED = 4
        COMPLETED_WITH_ERRORS = 5
        CANCELED = 6
        TIMED_OUT = 7

    class InstanceDetailsSummary(proto.Message):
        r"""A summary of the current patch state across all instances that this
        patch job affects. Contains counts of instances in different states.
        These states map to ``InstancePatchState``. List patch job instance
        details to see the specific states of each instance.

        Attributes:
            pending_instance_count (int):
                Number of instances pending patch job.
            inactive_instance_count (int):
                Number of instances that are inactive.
            notified_instance_count (int):
                Number of instances notified about patch job.
            started_instance_count (int):
                Number of instances that have started.
            downloading_patches_instance_count (int):
                Number of instances that are downloading
                patches.
            applying_patches_instance_count (int):
                Number of instances that are applying
                patches.
            rebooting_instance_count (int):
                Number of instances rebooting.
            succeeded_instance_count (int):
                Number of instances that have completed
                successfully.
            succeeded_reboot_required_instance_count (int):
                Number of instances that require reboot.
            failed_instance_count (int):
                Number of instances that failed.
            acked_instance_count (int):
                Number of instances that have acked and will
                start shortly.
            timed_out_instance_count (int):
                Number of instances that exceeded the time
                out while applying the patch.
            pre_patch_step_instance_count (int):
                Number of instances that are running the pre-
                atch step.
            post_patch_step_instance_count (int):
                Number of instances that are running the
                post-patch step.
            no_agent_detected_instance_count (int):
                Number of instances that do not appear to be
                running the agent. Check to ensure that the
                agent is installed, running, and able to
                communicate with the service.
        """

        pending_instance_count = proto.Field(proto.INT64, number=1)
        inactive_instance_count = proto.Field(proto.INT64, number=2)
        notified_instance_count = proto.Field(proto.INT64, number=3)
        started_instance_count = proto.Field(proto.INT64, number=4)
        downloading_patches_instance_count = proto.Field(proto.INT64, number=5)
        applying_patches_instance_count = proto.Field(proto.INT64, number=6)
        rebooting_instance_count = proto.Field(proto.INT64, number=7)
        succeeded_instance_count = proto.Field(proto.INT64, number=8)
        succeeded_reboot_required_instance_count = proto.Field(proto.INT64, number=9)
        failed_instance_count = proto.Field(proto.INT64, number=10)
        acked_instance_count = proto.Field(proto.INT64, number=11)
        timed_out_instance_count = proto.Field(proto.INT64, number=12)
        pre_patch_step_instance_count = proto.Field(proto.INT64, number=13)
        post_patch_step_instance_count = proto.Field(proto.INT64, number=14)
        no_agent_detected_instance_count = proto.Field(proto.INT64, number=15)

    name = proto.Field(proto.STRING, number=1)
    display_name = proto.Field(proto.STRING, number=14)
    description = proto.Field(proto.STRING, number=2)
    create_time = proto.Field(proto.MESSAGE, number=3, message=timestamp.Timestamp)
    update_time = proto.Field(proto.MESSAGE, number=4, message=timestamp.Timestamp)
    state = proto.Field(proto.ENUM, number=5, enum=State)
    instance_filter = proto.Field(
        proto.MESSAGE, number=13, message="PatchInstanceFilter"
    )
    patch_config = proto.Field(proto.MESSAGE, number=7, message="PatchConfig")
    duration = proto.Field(proto.MESSAGE, number=8, message=gp_duration.Duration)
    instance_details_summary = proto.Field(
        proto.MESSAGE, number=9, message=InstanceDetailsSummary
    )
    dry_run = proto.Field(proto.BOOL, number=10)
    error_message = proto.Field(proto.STRING, number=11)
    percent_complete = proto.Field(proto.DOUBLE, number=12)
    patch_deployment = proto.Field(proto.STRING, number=15)


class PatchConfig(proto.Message):
    r"""Patch configuration specifications. Contains details on how
    to apply the patch(es) to a VM instance.

    Attributes:
        reboot_config (~.gco_patch_jobs.PatchConfig.RebootConfig):
            Post-patch reboot settings.
        apt (~.gco_patch_jobs.AptSettings):
            Apt update settings. Use this setting to override the
            default ``apt`` patch rules.
        yum (~.gco_patch_jobs.YumSettings):
            Yum update settings. Use this setting to override the
            default ``yum`` patch rules.
        goo (~.gco_patch_jobs.GooSettings):
            Goo update settings. Use this setting to override the
            default ``goo`` patch rules.
        zypper (~.gco_patch_jobs.ZypperSettings):
            Zypper update settings. Use this setting to override the
            default ``zypper`` patch rules.
        windows_update (~.gco_patch_jobs.WindowsUpdateSettings):
            Windows update settings. Use this override
            the default windows patch rules.
        pre_step (~.gco_patch_jobs.ExecStep):
            The ``ExecStep`` to run before the patch update.
        post_step (~.gco_patch_jobs.ExecStep):
            The ``ExecStep`` to run after the patch update.
    """

    class RebootConfig(proto.Enum):
        r"""Post-patch reboot settings."""
        REBOOT_CONFIG_UNSPECIFIED = 0
        DEFAULT = 1
        ALWAYS = 2
        NEVER = 3

    reboot_config = proto.Field(proto.ENUM, number=1, enum=RebootConfig)
    apt = proto.Field(proto.MESSAGE, number=3, message="AptSettings")
    yum = proto.Field(proto.MESSAGE, number=4, message="YumSettings")
    goo = proto.Field(proto.MESSAGE, number=5, message="GooSettings")
    zypper = proto.Field(proto.MESSAGE, number=6, message="ZypperSettings")
    windows_update = proto.Field(
        proto.MESSAGE, number=7, message="WindowsUpdateSettings"
    )
    pre_step = proto.Field(proto.MESSAGE, number=8, message="ExecStep")
    post_step = proto.Field(proto.MESSAGE, number=9, message="ExecStep")


class Instance(proto.Message):
    r"""Namespace for instance state enums."""

    class PatchState(proto.Enum):
        r"""Patch state of an instance."""
        PATCH_STATE_UNSPECIFIED = 0
        PENDING = 1
        INACTIVE = 2
        NOTIFIED = 3
        STARTED = 4
        DOWNLOADING_PATCHES = 5
        APPLYING_PATCHES = 6
        REBOOTING = 7
        SUCCEEDED = 8
        SUCCEEDED_REBOOT_REQUIRED = 9
        FAILED = 10
        ACKED = 11
        TIMED_OUT = 12
        RUNNING_PRE_PATCH_STEP = 13
        RUNNING_POST_PATCH_STEP = 14
        NO_AGENT_DETECTED = 15


class CancelPatchJobRequest(proto.Message):
    r"""Message for canceling a patch job.

    Attributes:
        name (str):
            Required. Name of the patch in the form
            ``projects/*/patchJobs/*``
    """

    name = proto.Field(proto.STRING, number=1)


class AptSettings(proto.Message):
    r"""Apt patching is completed by executing
    ``apt-get update && apt-get upgrade``. Additional options can be set
    to control how this is executed.

    Attributes:
        type (~.gco_patch_jobs.AptSettings.Type):
            By changing the type to DIST, the patching is performed
            using ``apt-get dist-upgrade`` instead.
        excludes (Sequence[str]):
            List of packages to exclude from update.
            These packages will be excluded
        exclusive_packages (Sequence[str]):
            An exclusive list of packages to be updated.
            These are the only packages that will be
            updated. If these packages are not installed,
            they will be ignored. This field cannot be
            specified with any other patch configuration
            fields.
    """

    class Type(proto.Enum):
        r"""Apt patch type."""
        TYPE_UNSPECIFIED = 0
        DIST = 1
        UPGRADE = 2

    type = proto.Field(proto.ENUM, number=1, enum=Type)
    excludes = proto.RepeatedField(proto.STRING, number=2)
    exclusive_packages = proto.RepeatedField(proto.STRING, number=3)


class YumSettings(proto.Message):
    r"""Yum patching is performed by executing ``yum update``. Additional
    options can be set to control how this is executed.

    Note that not all settings are supported on all platforms.

    Attributes:
        security (bool):
            Adds the ``--security`` flag to ``yum update``. Not
            supported on all platforms.
        minimal (bool):
            Will cause patch to run ``yum update-minimal`` instead.
        excludes (Sequence[str]):
            List of packages to exclude from update. These packages are
            excluded by using the yum ``--exclude`` flag.
        exclusive_packages (Sequence[str]):
            An exclusive list of packages to be updated.
            These are the only packages that will be
            updated. If these packages are not installed,
            they will be ignored. This field must not be
            specified with any other patch configuration
            fields.
    """

    security = proto.Field(proto.BOOL, number=1)
    minimal = proto.Field(proto.BOOL, number=2)
    excludes = proto.RepeatedField(proto.STRING, number=3)
    exclusive_packages = proto.RepeatedField(proto.STRING, number=4)


class GooSettings(proto.Message):
    r"""Googet patching is performed by running ``googet update``."""


class ZypperSettings(proto.Message):
    r"""Zypper patching is performed by running ``zypper patch``. See also
    https://en.opensuse.org/SDB:Zypper_manual.

    Attributes:
        with_optional (bool):
            Adds the ``--with-optional`` flag to ``zypper patch``.
        with_update (bool):
            Adds the ``--with-update`` flag, to ``zypper patch``.
        categories (Sequence[str]):
            Install only patches with these categories.
            Common categories include security, recommended,
            and feature.
        severities (Sequence[str]):
            Install only patches with these severities.
            Common severities include critical, important,
            moderate, and low.
        excludes (Sequence[str]):
            List of patches to exclude from update.
        exclusive_patches (Sequence[str]):
            An exclusive list of patches to be updated. These are the
            only patches that will be installed using 'zypper patch
            patch:<patch_name>' command. This field must not be used
            with any other patch configuration fields.
    """

    with_optional = proto.Field(proto.BOOL, number=1)
    with_update = proto.Field(proto.BOOL, number=2)
    categories = proto.RepeatedField(proto.STRING, number=3)
    severities = proto.RepeatedField(proto.STRING, number=4)
    excludes = proto.RepeatedField(proto.STRING, number=5)
    exclusive_patches = proto.RepeatedField(proto.STRING, number=6)


class WindowsUpdateSettings(proto.Message):
    r"""Windows patching is performed using the Windows Update Agent.

    Attributes:
        classifications (Sequence[~.gco_patch_jobs.WindowsUpdateSettings.Classification]):
            Only apply updates of these windows update
            classifications. If empty, all updates are
            applied.
        excludes (Sequence[str]):
            List of KBs to exclude from update.
        exclusive_patches (Sequence[str]):
            An exclusive list of kbs to be updated. These
            are the only patches that will be updated. This
            field must not be used with other patch
            configurations.
    """

    class Classification(proto.Enum):
        r"""Microsoft Windows update classifications as defined in [1]
        https://support.microsoft.com/en-us/help/824684/description-of-the-standard-terminology-that-is-used-to-describe-micro
        """
        CLASSIFICATION_UNSPECIFIED = 0
        CRITICAL = 1
        SECURITY = 2
        DEFINITION = 3
        DRIVER = 4
        FEATURE_PACK = 5
        SERVICE_PACK = 6
        TOOL = 7
        UPDATE_ROLLUP = 8
        UPDATE = 9

    classifications = proto.RepeatedField(proto.ENUM, number=1, enum=Classification)
    excludes = proto.RepeatedField(proto.STRING, number=2)
    exclusive_patches = proto.RepeatedField(proto.STRING, number=3)


class ExecStep(proto.Message):
    r"""A step that runs an executable for a PatchJob.

    Attributes:
        linux_exec_step_config (~.gco_patch_jobs.ExecStepConfig):
            The ExecStepConfig for all Linux VMs targeted
            by the PatchJob.
        windows_exec_step_config (~.gco_patch_jobs.ExecStepConfig):
            The ExecStepConfig for all Windows VMs
            targeted by the PatchJob.
    """

    linux_exec_step_config = proto.Field(
        proto.MESSAGE, number=1, message="ExecStepConfig"
    )
    windows_exec_step_config = proto.Field(
        proto.MESSAGE, number=2, message="ExecStepConfig"
    )


class ExecStepConfig(proto.Message):
    r"""Common configurations for an ExecStep.

    Attributes:
        local_path (str):
            An absolute path to the executable on the VM.
        gcs_object (~.gco_patch_jobs.GcsObject):
            A Cloud Storage object containing the
            executable.
        allowed_success_codes (Sequence[int]):
            Defaults to [0]. A list of possible return values that the
            execution can return to indicate a success.
        interpreter (~.gco_patch_jobs.ExecStepConfig.Interpreter):
            The script interpreter to use to run the script. If no
            interpreter is specified the script will be executed
            directly, which will likely only succeed for scripts with
            [shebang lines]
            (https://en.wikipedia.org/wiki/Shebang_(Unix)).
    """

    class Interpreter(proto.Enum):
        r"""The interpreter used to execute the a file."""
        INTERPRETER_UNSPECIFIED = 0
        SHELL = 1
        POWERSHELL = 2

    local_path = proto.Field(proto.STRING, number=1)
    gcs_object = proto.Field(proto.MESSAGE, number=2, message="GcsObject")
    allowed_success_codes = proto.RepeatedField(proto.INT32, number=3)
    interpreter = proto.Field(proto.ENUM, number=4, enum=Interpreter)


class GcsObject(proto.Message):
    r"""Cloud Storage object representation.

    Attributes:
        bucket (str):
            Required. Bucket of the Cloud Storage object.
        object (str):
            Required. Name of the Cloud Storage object.
        generation_number (int):
            Required. Generation number of the Cloud
            Storage object. This is used to ensure that the
            ExecStep specified by this PatchJob does not
            change.
    """

    bucket = proto.Field(proto.STRING, number=1)
    object = proto.Field(proto.STRING, number=2)
    generation_number = proto.Field(proto.INT64, number=3)


class PatchInstanceFilter(proto.Message):
    r"""A filter to target VM instances for patching. The targeted
    VMs must meet all criteria specified. So if both labels and
    zones are specified, the patch job targets only VMs with those
    labels and in those zones.

    Attributes:
        all (bool):
            Target all VM instances in the project. If
            true, no other criteria is permitted.
        group_labels (Sequence[~.gco_patch_jobs.PatchInstanceFilter.GroupLabel]):
            Targets VM instances matching ANY of these
            GroupLabels. This allows targeting of disparate
            groups of VM instances.
        zones (Sequence[str]):
            Targets VM instances in ANY of these zones.
            Leave empty to target VM instances in any zone.
        instances (Sequence[str]):
            Targets any of the VM instances specified. Instances are
            specified by their URI in the form
            ``zones/[ZONE]/instances/[INSTANCE_NAME],``\ projects/[PROJECT_ID]/zones/[ZONE]/instances/[INSTANCE_NAME]\ ``, or``\ https://www.googleapis.com/compute/v1/projects/[PROJECT_ID]/zones/[ZONE]/instances/[INSTANCE_NAME]\`
        instance_name_prefixes (Sequence[str]):
            Targets VMs whose name starts with one of
            these prefixes. Similar to labels, this is
            another way to group VMs when targeting configs,
            for example prefix="prod-".
    """

    class GroupLabel(proto.Message):
        r"""Targets a group of VM instances by using their `assigned
        labels <https://cloud.google.com/compute/docs/labeling-resources>`__.
        Labels are key-value pairs. A ``GroupLabel`` is a combination of
        labels that is used to target VMs for a patch job.

        For example, a patch job can target VMs that have the following
        ``GroupLabel``: ``{"env":"test", "app":"web"}``. This means that the
        patch job is applied to VMs that have both the labels ``env=test``
        and ``app=web``.

        Attributes:
            labels (Sequence[~.gco_patch_jobs.PatchInstanceFilter.GroupLabel.LabelsEntry]):
                Compute Engine instance labels that must be
                present for a VM instance to be targeted by this
                filter.
        """

        labels = proto.MapField(proto.STRING, proto.STRING, number=1)

    all = proto.Field(proto.BOOL, number=1)
    group_labels = proto.RepeatedField(proto.MESSAGE, number=2, message=GroupLabel)
    zones = proto.RepeatedField(proto.STRING, number=3)
    instances = proto.RepeatedField(proto.STRING, number=4)
    instance_name_prefixes = proto.RepeatedField(proto.STRING, number=5)


__all__ = tuple(sorted(__protobuf__.manifest))
